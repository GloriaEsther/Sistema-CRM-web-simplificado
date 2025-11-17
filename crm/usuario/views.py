from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm
from .models import Usuario, PreferenciaUsuario
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles# es un decorador de roles y el login_required simple.
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

def registrar_usuario(request):#funciona
   # Validar que haya sesión activa
    user_id = request.session.get('idusuario')
    if not user_id:
        messages.error(request, "Debes iniciar sesión.")
        return redirect('usuario:iniciar_sesion')

    #Validar que el usuario actual exista y esté activo
    usuario_actual = Usuario.activos.filter(idusuario=user_id).first()
    if not usuario_actual:
        messages.error(request, "Tu sesión expiró. Inicia sesión nuevamente.")
        request.session.flush()
        return redirect('usuario:iniciar_sesion')

    #Validar roles permitidos
    if request.session.get('rol') not in ['Dueño', 'Administrador']:
        messages.error(request, "No tienes permisos para registrar usuarios.")
        return redirect('usuario:inicio')

    #Se procesa el formulario
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                nuevo_usuario = form.save(commit=False)#Obtiene el objeto pero aun no lo guarda en la base de datos (se van a agregar cosas :b)
                 # Registrar quién lo creó
                nuevo_usuario.usuario_registro = usuario_actual
                nuevo_usuario.save()

                messages.success(request, f"Usuario {nuevo_usuario.nombre} registrado correctamente.")
                '''
                return render(request, 'usuario/registrar_usuario.html', {
                    'form': UsuarioForm(),  
                    'mostrar_modal': True,
                })
                esto estaba antes
                '''
                return redirect('usuario:registrar_usuario')         
            except IntegrityError:
               messages.error(request, "Ocurrio un error :(")
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = UsuarioForm()
    return render(request, 'usuario/registrar_usuario.html', {'form': form})

def iniciar_sesion(request):#funciona

    # Si ya está logueado -> redirigir
    if request.session.get('idusuario'):
        return redirect('usuario:inicio')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            # 1) Verificar usuario
            usuario = Usuario.activos.filter(correo=correo).first()
            if not usuario:
                messages.error(request, "No existe una cuenta con ese correo.")
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Cuenta no encontrada',
                    'modal_mensaje': 'No existe una cuenta con ese correo electrónico.'
                })

            # 2) Verificar contraseña
            if not check_password(contrasena, usuario.contrasena):
                messages.error(request, "Contraseña incorrecta.")
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Contraseña incorrecta',
                    'modal_mensaje': 'La contraseña ingresada no es válida.'
                })

            # 3) Limpiar cualquier sesión previa
            request.session.flush()

            # 4) Crear sesión nueva
            request.session['idusuario'] = usuario.idusuario
            request.session['nombre'] = usuario.nombre
            request.session['rol'] = usuario.rol.nombre_rol

            messages.success(request, f"Bienvenido {usuario.nombre}")
            return redirect('usuario:inicio')

    else:
        form = LoginForm()

    return render(request, 'usuario/login.html', {'form': form})

#@require_roles(['Dueño', 'Administrador'])
def listar_usuarios(request):#consultar usuarios (en lo basico si funciona)
    usuarios = Usuario.activos.all().order_by('idusuario')
    return render(request, 'usuario/listar_usuarios.html', {'usuarios': usuarios})

@require_roles(['Dueño', 'Administrador'])
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario modificado correctamente.")
            return redirect('usuario:listar_usuarios')
        else:
            messages.error(request, "Revisa los errores del formulario.")
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'usuario/editar_usuario.html', {
        'form': form,
        'usuario': usuario
    })


@require_roles(['Dueño'])
def eliminar_usuario(request, pk):#funciona
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.eliminar_logico()
    messages.success(request, "Usuario eliminado ")#"(lógicamente)."
    return redirect('usuario:listar_usuarios')

def cerrar_sesion(request):#funciona
    request.session.flush()  # borra la sesión
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('usuario:iniciar_sesion')

def subir_logo(request):
    if request.method == "POST" and request.FILES.get("logo"):

        archivo = request.FILES["logo"]
        fs = FileSystemStorage(location="media/logos")
        filename = fs.save(archivo.name, archivo)

        # Guardamos en sesión para mostrarlo siempre
        request.session["logo"] = "/media/logos/" + filename

        return redirect('inicio')

    return redirect('inicio')

def inicio(request):
    
    usuario = None
    preferencias = None

    if request.session.get("idusuario"):
        usuario = Usuario.activos.get(idusuario=request.session["idusuario"])

        preferencias, creado = PreferenciaUsuario.objects.get_or_create(usuario=usuario)

        if request.method == "POST":
            preferencias.color_primario = request.POST.get("color_primario", preferencias.color_primario)
            preferencias.color_secundario = request.POST.get("color_secundario", preferencias.color_secundario)
            preferencias.color_fondo = request.POST.get("color_fondo", preferencias.color_fondo)

            if "logo" in request.FILES:
                preferencias.logo = request.FILES["logo"]

            preferencias.save()

            return redirect("usuario:inicio")#return redirect("inicio")

    return render(request, "inicio.html", {
        "usuario": usuario,
        "preferencias": preferencias
    })
