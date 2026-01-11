from django.shortcuts import render,redirect, get_object_or_404
from .forms import UsuarioForm,LoginForm,EmpleadoForm
from .models import Usuario, PreferenciaUsuario,RolUsuario
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles,queryset_empleados_por_rol
from django.contrib import messages
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
                nuevo_usuario.save()            
                return redirect('oportunidades:kanban')               
            except IntegrityError:
                messages.error(request, "Error: Usuario ya existente")
                return render(request, 'usuario/registrar_usuario.html', {'form': form, 'duplicado': True})     
            except Exception as e:
                messages.error(request, f"Ocurrió un error inesperado al registrar: {e}")

    else:
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
    
    if request.method == 'POST':
        form = LoginForm(request.POST)   
        
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contrasena = form.cleaned_data['contrasena']
            #Verificar usuario y contraseña 
            usuario = Usuario.activos.filter(correo=correo).first()
            
            if usuario and check_password(contrasena, usuario.contrasena):
                request.session.flush()
                request.session['idusuario'] = usuario.idusuario
                request.session['nombre'] = usuario.nombre
                request.session['rol'] = usuario.rol.nombre_rol 
                
                # Redirección según rol
                if usuario.rol.nombre_rol == "Superusuario":
                    return redirect('superusuario:dashboard')
                return redirect('oportunidades:kanban')
                              
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

@require_roles(['Dueño'])
def perfil_usuario(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    return render(request, "usuario/perfil.html", {
        "usuario": usuario
    })

@require_roles(['Dueño'])
def editar_perfil(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("usuario:perfil")
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, "usuario/editar_perfil.html", {
        "form": form
    })

@require_roles(['Dueño'])#@require_roles(['Dueño', 'Administrador'])
def editar_empleado(request, pk):
    empleado = Usuario.activos.filter(idusuario=pk).first()

    if not empleado:
        messages.error(request, "Empleado no encontrado.")
        return redirect("usuario:empleados_lista")

    if request.method == "POST":
        form = EmpleadoForm(request.POST, instance=empleado)
        if form.is_valid():
            form.save()
            messages.success(request, "Empleado actualizado correctamente.")
            return redirect("usuario:empleados_lista")
    else:
        form = EmpleadoForm(instance=empleado)

    return render(request, "usuario/editar_empleado.html", {
        "form": form,
        "empleado": empleado
    })

@require_roles(['Dueño'])#@require_roles(['Dueño', 'Administrador'])
def consultar_empleado(request, pk):#def consultar_empleado(request, idusuario):
    empleado = Usuario.activos.filter(idusuario=pk).first()

    if not empleado:
        messages.error(request, "Empleado no encontrado.")
        return redirect("usuario:empleados_lista")

    return render(request, "usuario/consultar_empleado.html", {
        "empleado": empleado
    })

@require_roles(['Dueño'])
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    usuario.eliminar_logico()
    messages.success(request, "Usuario eliminado ")
    return redirect('usuario:empleados_lista')

def cerrar_sesion(request):
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

    return render(request, "inicio.html", {
        "user": usuario, 
        "preferencias": preferencias
    })

def agregar_empleado(request):#solo el dueno puede registrar empleados
    usuario_id = request.session.get('idusuario')
    usuario=Usuario.activos.get(idusuario=usuario_id)
    # Regla por rol
    es_dueno = usuario.rol.nombre_rol == "Dueño" 
    es_admin = usuario.rol.nombre_rol == "Administrador"
    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)

            if es_dueno:
              empleado.owner_id = usuario

            if es_admin:# asignar  del dueno
              empleado.owner_id = usuario.owner_id      

            empleado.save()
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('oportunidades:kanban')
    else:
        form = EmpleadoForm()

    return render(request, "usuario/agregar_empleado.html", {"form": form})

def empleados_lista(request):
    usuario = Usuario.activos.filter(
        idusuario=request.session.get("idusuario")
    ).first()

    empleados = queryset_empleados_por_rol(usuario)

    return render(request, "usuario/empleados_lista.html", {
        "empleados": empleados
    })
