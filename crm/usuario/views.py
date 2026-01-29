from django.shortcuts import render,redirect
from .forms import UsuarioForm,LoginForm,EmpleadoForm
from .models import Usuario, PreferenciaUsuario,RolUsuario
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import check_password 
from crm.utils import require_roles,queryset_empleados_por_rol,obtener_owner,obtener_usuario_perfil
from django.contrib import messages
from django.utils import timezone

def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                nuevo_usuario = form.save(commit=False)
                rol_dueno = RolUsuario.objects.filter(nombre_rol__iexact="Dueño").first()
                nuevo_usuario.owner_id = None
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
    #Verificar si ya hay una sesión activa ANTES de hacer cualquier cosa
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

@require_roles(['Dueño','Superusuario'])
def perfil_usuario(request):
    usuario_objetivo = obtener_usuario_perfil(request)
    return render(request, "usuario/perfil.html", {
        "usuario": usuario_objetivo
    })

@require_roles(['Dueño','Superusuario'])
def editar_perfil(request):
    usuario_objetivo = obtener_usuario_perfil(request)

    if request.method == "POST":
        form = UsuarioForm(request.POST, instance=usuario_objetivo)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil actualizado correctamente.")
            return redirect("usuario:perfil")
    else:
        form = UsuarioForm(instance=usuario_objetivo)

    return render(request, "usuario/editar_perfil.html", {
        "form": form,
        "usuario": usuario_objetivo
    })

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
    return redirect('oportunidades:kanban') 

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

#Empleado
def empleados_lista(request):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)
    if not owner:
        empleados = Usuario.activos.none()
    else:
        empleados = queryset_empleados_por_rol(usuario,owner)

    return render(request, "usuario/lista_empleados.html", {
        "empleados": empleados
    })

def agregar_empleado(request):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    if not owner:
        messages.error(request, "No hay negocio seleccionado.")
        return redirect("superusuario:listar_negocios")

    if request.method == "POST":
        form = EmpleadoForm(request.POST)
        if form.is_valid():
            empleado = form.save(commit=False)
            empleado.owner_id = owner   
            empleado.save()
            messages.success(request, "Empleado agregado correctamente.")
            return redirect('usuario:empleados_lista')
    else:
        form = EmpleadoForm()

    return render(request, "usuario/empleado.html", {
        "form": form,
        "modo": "crear"
    })

@require_roles(['Dueño', 'Superusuario'])
def consultar_empleado(request, pk):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    empleado = Usuario.activos.filter(
        idusuario=pk,
        owner_id=owner
    ).first()

    if not empleado:
        messages.error(request, "Empleado no encontrado.")
        return redirect("usuario:empleados_lista")

    return render(request, "usuario/consultar_empleado.html", {
        "empleado": empleado
    })

@require_roles(['Dueño', 'Superusuario'])
def editar_empleado(request, pk):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    empleado = Usuario.activos.filter(
        idusuario=pk,
        owner_id=owner
    ).first()

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

    return render(request, "usuario/empleado.html", {
        "form": form,
        "modo": "editar",
        "empleado": empleado
    })

@require_roles(['Dueño', 'Superusuario'])
def eliminar_usuario(request, pk):
    usuario = Usuario.activos.get(idusuario=request.session["idusuario"])
    owner = obtener_owner(request, usuario)

    empleado = Usuario.activos.filter(
        idusuario=pk,
        owner_id=owner
    ).first()

    if not empleado:
        messages.error(request, "Usuario no encontrado.")
        return redirect("usuario:empleados_lista")

    empleado.eliminar_logico()
    messages.success(request, "Usuario eliminado")
    return redirect("usuario:empleados_lista")