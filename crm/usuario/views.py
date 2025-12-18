from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm,EmpleadoForm
from .models import Usuario, PreferenciaUsuario,RolUsuario
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles# es un decorador de roles y el login_required simple.
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.utils import timezone

def registrar_usuario(request):#usuario=dueño del micronegocio
    usuario_id = request.session.get('idusuario')
    usuario =Usuario.activos.filter(idusuario=usuario_id).first()
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                nuevo_usuario = form.save(commit=False)
                rol_dueno = RolUsuario.objects.filter(nombre_rol__iexact="Dueño").first()
                nuevo_usuario.owner_id = None#dueno no tiene owner_id
                nuevo_usuario.rol = rol_dueno
                print("ANTES DEL SAVE:", nuevo_usuario.idusuario)
                nuevo_usuario.save()
                print("DESPUÉS DEL SAVE:", nuevo_usuario.idusuario)
                #messages.success(request, f"Usuario {nuevo_usuario.nombre} registrado correctamente.")               
                return redirect('oportunidades:kanban')               
            except IntegrityError:
                messages.error(request, "Error: Usuario ya existente")
                return render(request, 'usuario/registrar_usuario.html', {'form': form, 'duplicado': True})     
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar: {e}")

    else: # GET request
        form = UsuarioForm()
    return render(request, 'usuario/registrar_usuario.html', {
        'form': form
    })


def iniciar_sesion(request):
    #Verificar si ya hay una sesión activa ANTES de hacer cualquier query
    usuario_id = request.session.get('idusuario')
    rol_sesion = request.session.get('rol')

    if usuario_id:
        if rol_sesion == "Superusuario":
            return redirect('superusuario:dashboard')
        return redirect('oportunidades:kanban')
    #if request.session.get('idusuario'):#esto funcionaba...
    #    return redirect('oportunidades:kanban')#pipeline ventas
    if request.method == 'POST':
        form = LoginForm(request.POST)   
        
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            #Verificar usuario y contraseña 
            usuario = Usuario.activos.filter(correo=correo).first()
            
            if usuario and check_password(contrasena, usuario.contrasena):
                request.session.flush()
                #Crear sesión nueva 
                #Guardar datos en sesion
                request.session['idusuario'] = usuario.idusuario
                request.session['nombre'] = usuario.nombre
                request.session['rol'] = usuario.rol.nombre_rol #esto es para el decorador
               # messages.success(request, f"Bienvenido {usuario.nombre}")
                
                # Redirección según rol
                if usuario.rol.nombre_rol == "Superusuario":
                    return redirect('superusuario:dashboard')
                return redirect('oportunidades:kanban')
                              
               # return redirect('oportunidades:kanban') # Usar dashboard en lugar de inicio
            else:
                #messages.error(request, "Credenciales incorrectas (correo o contraseña).")
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Error de Ingreso',
                    'modal_mensaje': 'Verifica tu correo electrónico o contraseña.'
                })
    else:
        form = LoginForm()

    return render(request, 'usuario/login.html', {
        'form': form,
        'timestamp': timezone.now().timestamp()
    })

@require_roles(['Dueño', 'Administrador'])
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
    #
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
        
        if not request.session.get("idusuario"):
            return redirect('usuario:iniciar_sesion') 

        usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
        if usuario.rol.nombre_rol != "Dueño":
            return redirect("usuario:inicio")

        preferencias, _ = PreferenciaUsuario.objects.get_or_create(
            usuario=usuario
        )

        preferencias.logo = request.FILES["logo"]
        preferencias.save()
    return redirect('oportunidades:kanban') #return redirect('usuario:inicio') 

def inicio(request):  
    usuario = None
    preferencias = None

    if request.session.get("idusuario"):
        # Aseguramos que el usuario aún exista
        try:
            usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
            preferencias, creado = PreferenciaUsuario.objects.get_or_create(usuario=usuario)
        except Usuario.DoesNotExist:
            # Si el usuario de la sesión no existe, limpiamos la sesión
            request.session.flush()
            messages.error(request, "Tu sesión es inválida. Inicia sesión.")
            return redirect('usuario:iniciar_sesion')
            
        if request.method == "POST":
            # Esto es para guardar las preferencias de color, no el logo (el logo tiene su propia vista)
            preferencias.color_primario = request.POST.get("color_primario", preferencias.color_primario)
            preferencias.color_secundario = request.POST.get("color_secundario", preferencias.color_secundario)
            preferencias.color_fondo = request.POST.get("color_fondo", preferencias.color_fondo)

            preferencias.save()
            messages.success(request, "Preferencias de diseño guardadas.")
            return redirect("usuario:inicio")

    # Si NO está logueado, o si es un GET, renderiza la página
    return render(request, "inicio.html", {
        "user": usuario, # <--- CAMBIAR a 'user' si usas user.is_authenticated en el template
        "preferencias": preferencias
    })

def agregar_empleado(request):#solo el dueno puede registrar empleados
    usuario_id = request.session.get('idusuario')
    usuario=Usuario.activos.get(idusuario=usuario_id)
    # Regla por rol
    es_dueno = usuario.rol.nombre_rol == "Dueño" #in ["Dueño"]
    es_admin = usuario.rol.nombre_rol == "Administrador"
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)

            if es_dueno:# asignar dueño
              empleado.owner_id = usuario#owner_id#empleado.owner_id = usuario

            if es_admin:# asignar  del dueno
              empleado.owner_id = usuario.owner_id      

            empleado.save()
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('oportunidades:kanban')#return redirect('usuario:listar_usuarios')
    else:
        form = EmpleadoForm()

    return render(request, "usuario/agregar_empleado.html", {"form": form})
