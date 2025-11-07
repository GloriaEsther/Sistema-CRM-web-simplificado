from django.shortcuts import render,redirect
from .forms import UsuarioForm,LoginForm
from .models import Usuario
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password

@csrf_exempt
def registrar_usuario(request):
    mostrar_modal = False
    clave = None
    duplicado = False
    campo_duplicado = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        
        if form.is_valid():
            try:
                usuario = form.save(commit=False)#Obtiene el objeto pero aun no lo guarda en la base de datos (se van a agregar cosas :b)
                usuario.save()#ahora si lo va a guardar en la base 
                clave = usuario.claveusuario
                
                mostrar_modal = True
                # Renderizamos la plantilla con la clave y un indicador para mostrar el modal
                return render(request, 'usuario/registrar_usuario.html', {
                    'form': UsuarioForm(),  # formulario vacío
                    'mostrar_modal': mostrar_modal,
                    'claveusuario': clave
                })         
            except IntegrityError as e:
                duplicado = True
                data = request.POST
                correo = data.get('correo')
                rfc = data.get('rfc')
                curp = data.get('curp')
                
                if Usuario.activos.filter(correo=correo).exists():
                    campo_duplicado = "correo electrónico"
                elif Usuario.activos.filter(rfc=rfc).exists():
                    campo_duplicado = "RFC"
                elif Usuario.activos.filter(curp=curp).exists():
                    campo_duplicado = "CURP"
                else:
                    campo_duplicado = "alguno de los datos"
               # messages.error(request, "a existe un usuario con el correo, RFC o CURP ingresado.")
        else:

            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Error en {field}: {error}")
            
            errores_texto = form.errors.as_text()
            if "Ya existe un usuario" in errores_texto:
                duplicado = True
    else:
        form = UsuarioForm()

    return render(request, 'usuario/registrar_usuario.html', {''
        'form': form,
        'mostrar_modal': mostrar_modal,#lo mismo pero el modal :b
        'claveusuario': clave,
        'duplicado': duplicado,#activa el modal de duplicados en el html
        'campo_duplicado': campo_duplicado,
    })

@csrf_exempt
def iniciar_sesion(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        correo = request.POST.get('correo', '').strip()
        contrasena = request.POST.get('contrasena', '').strip()

        if not correo or not contrasena:
            return render(request, 'usuario/login.html', {
                'form': form,
                'mostrar_modal': True,
                'modal_titulo': 'Campos incompletos',
                'modal_mensaje': 'Por favor, completa todos los campos antes de continuar.'
            })
        
        if form.is_valid():
            correo = form.cleaned_data['correo']#correo = form.cleaned_data.get('correo')
            contrasena = form.cleaned_data['contrasena']#contrasena = form.cleaned_data.get('contrasena')

            try:
                usuario = Usuario.activos.get(correo=correo)

                if check_password(contrasena, usuario.contrasena):

                    request.session['idusuario'] = usuario.idusuario#request.session['usuario_id'] = usuario.idusuario
                    request.session['nombre'] = usuario.nombre#request.session['usuario_nombre'] = usuario.nombre
                    request.session['rol'] = usuario.rol#request.session['usuario_rol'] = usuario.rol

                    return render(request, 'usuario/login.html', {
                        'form': LoginForm(),
                        'mostrar_modal': True,
                        'modal_titulo': 'Inicio de sesión exitoso',
                        'modal_mensaje': f'¡Bienvenido, {usuario.nombre}! Serás redirigido en unos segundos...',
                        'redirigir': True
                    })
                else:
                    return render(request, 'usuario/login.html', {
                        'form': form,
                        'mostrar_modal': True,
                        'modal_titulo': 'Contraseña incorrecta',
                        'modal_mensaje': 'La contraseña ingresada no es válida.'
                    })
                    #messages.error(request, "Contraseña incorrecta.")
            except Usuario.DoesNotExist:
                return render(request, 'usuario/login.html', {
                    'form': form,
                    'mostrar_modal': True,
                    'modal_titulo': 'Cuenta no encontrada',
                    'modal_mensaje': 'No existe una cuenta con ese correo electrónico.'
                })
                #messages.error(request, "No existe una cuenta con ese correo, favor de registrarse.")
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
