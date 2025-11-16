from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm
from .models import Usuario, PreferenciaUsuario
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles# es un decorador de roles y el login_required simple.
from django.contrib import messages

@csrf_exempt
def registrar_usuario(request):
   
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()#(commit=False)#Obtiene el objeto pero aun no lo guarda en la base de datos (se van a agregar cosas :b)
                #usuario.contrasena = make_password(usuario.contrasena)
                usuario.save()

                messages.success(request, f"Usuario {usuario.nombre} registrado correctamente.")
                return render(request, 'usuario/registrar_usuario.html', {
                    'form': UsuarioForm(),  
                    'mostrar_modal': True,
                })         
            except IntegrityError:
               messages.error(request, "Ocurrio un error :(")
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
    else:
        form = UsuarioForm()
    return render(request, 'usuario/registrar_usuario.html', {'form': form})

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
        
            try:
                usuario = Usuario.activos.get(correo=correo)
            except Usuario.DoesNotExist:
                messages.error(request, "No existe una cuenta con ese correo, favor de registrarse.")
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Cuenta no encontrada',
                    'modal_mensaje': 'No existe una cuenta con ese correo electrónico.'
                })
            #messages.error(request, "No existe una cuenta con ese correo, favor de registrarse.")
            
            if check_password(contrasena, usuario.contrasena):
                    request.session['idusuario'] = usuario.idusuario
                    request.session['nombre'] = usuario.nombre
                    request.session['rol'] = usuario.rol.nombre_rol
                    messages.success(request, f"Bienvenido {usuario.nombre}")            
                    return redirect('inicio')
            else: 
                messages.error(request, "Contraseña incorrecta.")      
                return render(request, 'usuario/login.html', {
                        'form': form,
                        'mostrar_modal': True,
                        'modal_titulo': 'Contraseña incorrecta',
                        'modal_mensaje': 'La contraseña ingresada no es válida.'
                })             
            
    else:
        form=LoginForm()      
    return render(request, 'usuario/login.html', {'form': form})

#aun no los he probado
@require_roles(['Dueño', 'Administrador'])
def listar_usuarios(request):
    usuarios = Usuario.activos.all()
    return render(request, 'usuarios/listar.html', {'usuarios': usuarios})

@require_roles(['Dueño'])
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.eliminar_logico()
    messages.success(request, "Usuario eliminado ")#"(lógicamente)."
    return redirect('usuarios:listar_usuarios')

@csrf_exempt
def cerrar_sesion(request):#no funciono, mejor ahorita veo que hago.....
    request.session.flush()  # borra la sesión
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciar_sesion')#da este error:

@csrf_exempt
def inicio(request):#por ahora es prueba :)
    
    usuario = None
    preferencias = None
    # Si el usuario está logueado
    if "idusuario" in request.session:
        usuario = Usuario.activos.get(idusuario=request.session["idusuario"])

        # Obtiene o crea preferencias del usuario
        preferencias, creado = PreferenciaUsuario.objects.get_or_create(usuario=usuario)

        # Si el usuario envió cambios al formulario
        if request.method == "POST":

            # Guardar colores
            preferencias.color_primario = request.POST.get("color_primario", preferencias.color_primario)
            preferencias.color_secundario = request.POST.get("color_secundario", preferencias.color_secundario)
            preferencias.color_fondo = request.POST.get("color_fondo", preferencias.color_fondo)

            # Guardar logo
            if "logo" in request.FILES:
                preferencias.logo = request.FILES["logo"]

            preferencias.save()

            messages.success(request, "Preferencias guardadas correctamente.")
            return redirect("inicio")

    # Si no está logueado, solo muestra la pantalla sin preferencias
    return render(request, "inicio.html", {#intenta poner la direccion de inicio/ pero el de crm templates
        "usuario": usuario,
        "preferencias": preferencias})
    
    #return render (request,"inicio.html")    
