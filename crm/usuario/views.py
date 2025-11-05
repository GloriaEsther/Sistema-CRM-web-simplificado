from django.shortcuts import render,redirect
from .forms import UsuarioForm,LoginForm
from .models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password

@csrf_exempt
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                messages.success(request, f"Registro exitoso. Su clave es: {usuario.claveusuario}. Será redirigido al inicio de sesión en unos segundos...")
                # en lugar de redirigir de inmediato, renderizamos la misma plantilla con redirección diferida
                return render(request, 'usuario/registrar_usuario.html', {
                    'form': UsuarioForm(),  # formulario vacío
                    'redirigir': True
                })
            except IntegrityError:
                messages.error(request, "Error: datos duplicados.")
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
        #correo = request.POST.get('correo')
        #contrasena = request.POST.get('contrasena')
        form = LoginForm(request.POST)
        if not form.correo or not form.contrasena:
            messages.error(request, "Por favor, llena ambos campos.")
            return render(request, 'usuario/login.html')
        
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            try:
                usuario = Usuario.activos.get(correo=correo)
                if check_password(contrasena, usuario.contrasena):
                    request.session['usuario_id'] = usuario.idusuario
                    request.session['usuario_nombre'] = usuario.nombre
                    request.session['usuario_rol'] = usuario.rol
                    messages.success(request, f"¡Bienvenido, {usuario.nombre}!")
                    return redirect('inicio')  #vista principal
                else:
                    messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                messages.error(request, "No existe una cuenta con ese correo.")

        '''  try:
            usuario = Usuario.todos.get(correo=correo, activo=True)
            
            if check_password(contrasena, usuario.contrasena):
                request.session['usuario_id'] = usuario.idusuario
                request.session['nombre_usuario'] = usuario.nombre
                request.session['usuario_rol'] = usuario.rol
                messages.success(request, f"Bienvenido {usuario.nombre}")
                return redirect('inicio')
            else:
                messages.error(request, "Contraseña incorrecta.")
        except Usuario.DoesNotExist:
            messages.error(request, "El correo no está registrado.")
    
        '''
    else:
        form=LoginForm()      
    return render(request, 'usuario/login.html', {'form': form})

@csrf_exempt
def cerrar_sesion(request):
    request.session.flush()  # borra la sesión
    messages.success(request, "Has cerrado sesión.")
    return redirect('iniciar_sesion')

@csrf_exempt
def inicio(request):#por ahora es prueba :)
    return render (request,"inicio.html")    
