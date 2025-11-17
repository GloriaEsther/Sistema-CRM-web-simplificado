from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm
from .models import Usuario, PreferenciaUsuario
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles# es un decorador de roles y el login_required simple.
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

@require_roles(['Dueño'])
def registrar_usuario(request):
    usuario_registrador = request.user 
    
    # Si el usuario no está autenticado, el decorador ya lo redirigió. 
    # Si llega aquí, está autenticado y es Dueño.
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                nuevo_usuario = form.save(commit=False)
                # Asignar el Dueño logueado como el creador del registro
                nuevo_usuario.usuario_registro = usuario_registrador
                nuevo_usuario.save()

                messages.success(request, f"Usuario {nuevo_usuario.nombre} registrado correctamente.")
                # Redirigimos al mismo formulario para permitir que el Dueño siga registrando
                return redirect('usuario:registrar_usuario')
                                
            except IntegrityError:
                # Si falla la unicidad (correo, RFC, CURP, etc.)
                messages.error(request, "Error: Ya existe un usuario con uno de los datos ingresados (correo, RFC o CURP).")
                # Pasamos 'duplicado': True para que el template muestre el modal
                return render(request, 'usuario/registrar_usuario.html', {'form': form, 'duplicado': True})
            
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar: {e}")
        
    else: # GET request
        form = UsuarioForm()
    return render(request, 'usuario/registrar_usuario.html', {
        'form': form,
        # Si 'duplicado' no fue definido en el try/except, se asume False o se omite
        'duplicado': 'duplicado' in locals() 
    })

def iniciar_sesion(request):#funciona

    # Si ya está logueado -> redirigir
    if request.session.get('idusuario'):
        return redirect('oportunidades:kanban')#pipeline ventas

    if request.method == 'POST':
        form = LoginForm(request.POST)   
        
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']

            #Verificar usuario y contraseña (usando tu lógica actual)
            usuario = Usuario.activos.filter(correo=correo).first()
            
            if usuario and check_password(contrasena, usuario.contrasena):
                
                #Limpiar cualquier sesión previa
                request.session.flush()

                #Crear sesión nueva (USANDO TU LÓGICA PERSONALIZADA)
                request.session['idusuario'] = usuario.idusuario
                request.session['nombre'] = usuario.nombre
                request.session['rol'] = usuario.rol.nombre_rol

                messages.success(request, f"Bienvenido {usuario.nombre}")
                #Redirigir al inicio de la aplicación para usuarios logueados
                return redirect('oportunidades:kanban') # Usar dashboard en lugar de inicio
            else:
                # Error de credenciales
                messages.error(request, "Credenciales incorrectas (correo o contraseña).")
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Error de Ingreso',
                    'modal_mensaje': 'Verifica tu correo electrónico y contraseña.'
                })

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

'''
def subir_logo(request):
    if request.method == "POST" and request.FILES.get("logo"):

        archivo = request.FILES["logo"]
        fs = FileSystemStorage(location="media/logos")
        filename = fs.save(archivo.name, archivo)

        # Guardamos en sesión para mostrarlo siempre
        request.session["logo"] = "/media/logos/" + filename

        return redirect('inicio')

    return redirect('inicio')
'''

def subir_logo(request):
    # 1. Revisar que sea POST y que haya archivo
    if request.method == "POST" and request.FILES.get("logo"):
        
        # 2. Requerir que el usuario esté logueado (y exista en sesión)
        if not request.session.get("idusuario"):
            return redirect('usuario:iniciar_sesion') 

        try:
            # 3. Obtener el usuario y su objeto de preferencias
            usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
            preferencias, creado = PreferenciaUsuario.objects.get_or_create(usuario=usuario)
            
            # 4. Guardar el logo usando el FileField del modelo
            preferencias.logo = request.FILES["logo"]
            preferencias.save() # Django gestiona la subida al disco y la ruta en DB

        except Usuario.DoesNotExist:
             # Manejar si el idusuario de la sesión no existe
             pass 

    # 5. Redirigir de vuelta al inicio
    return redirect('usuario:inicio') # Redirección con namespace 'usuario'

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