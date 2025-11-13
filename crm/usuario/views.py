from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm
from .models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles# es un decorador de roles y el login_required simple.

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
        #correo = request.POST.get('correo', '').strip()
        #contrasena = request.POST.get('contrasena', '').strip()
        '''
        if not correo or not contrasena:
            return render(request, 'usuario/login.html', {
                'form': form,
                'mostrar_modal': True,
                'modal_titulo': 'Campos incompletos',
                'modal_mensaje': 'Por favor, completa todos los campos antes de continuar.'
            })
        '''
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
        
            try:
                usuario = Usuario.activos.get(correo=correo)
                '''
                if check_password(contrasena, usuario.contrasena):
                    request.session['idusuario'] = usuario.idusuario
                    request.session['nombre'] = usuario.nombre
                    request.session['rol'] = usuario.rol.nombre_rol
                    messages.success(request, f"Bienvenido {usuario.nombre}")
                    
                    return render(request, 'usuario/login.html', {
                            'form': LoginForm(),
                            'mostrar_modal': True,
                            'modal_titulo': 'Inicio de sesión exitoso',
                            'modal_mensaje': f'¡Bienvenido, {usuario.nombre}! Serás redirigido en unos segundos...',
                            'redirigir': True
                        })
                    
                    return redirect('inicio')  # Redirige al dashboard o inicio
                else:
                    
                    return render(request, 'usuario/login.html', {
                        'form': form,
                        'mostrar_modal': True,
                        'modal_titulo': 'Contraseña incorrecta',
                        'modal_mensaje': 'La contraseña ingresada no es válida.'
                    })
                    
                    #messages.error(request, "Contraseña incorrecta.")
           
                '''
            except Usuario.DoesNotExist:
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
                return render(request, 'usuario/login.html', {
                        'form': form,
                        'mostrar_modal': True,
                        'modal_titulo': 'Contraseña incorrecta',
                        'modal_mensaje': 'La contraseña ingresada no es válida.'
                })             
                #messages.error(request, "Contraseña incorrecta.")
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
def cerrar_sesion(request):
    request.session.flush()  # borra la sesión
    messages.success(request, "Has cerrado sesión correctamente.")
    return redirect('iniciar_sesion')

@csrf_exempt
def inicio(request):#por ahora es prueba :)
    return render (request,"inicio.html")    
