from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required as dj_login_required
from django.contrib.auth import logout
from usuario.models import Usuario,RolUsuario
from cliente.models import Cliente
from django.db.models import Q
from servicios.models import Servicio
from inventario.models import Inventario
from django.shortcuts import redirect

def require_roles(allowed_roles):#restringe roles (quien accede a que)
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            rol = request.session.get('rol') or (getattr(request.user, 'rol', None) and getattr(request.user.rol, 'nombre_rol', None))
            if rol not in allowed_roles:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                #FORZAMOS EL CIERRE DE SESIÓN si el usuario estaba logueado
                if request.user.is_authenticated:
                     logout(request) 
                #Redirigimos al LOGIN
                return redirect('usuario:iniciar_sesion')  
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator

def queryset_usuarios_segun_rol(usuario):#es un filtro en las busquedas de usuario
    rol = usuario.rol.nombre_rol
    negocio = usuario if rol == "Dueño" else usuario.owner_id
    
    if rol in ["Dueño", "Administrador"]:
        return Usuario.activos.filter(
            Q(idusuario=negocio.idusuario) |
            Q(owner_id=negocio.idusuario)
        )

    if rol == "Vendedor":
        return Usuario.activos.filter(idusuario=usuario.idusuario)

    return Usuario.activos.none()

def queryset_clientes_por_rol(usuario):#prueba
    rol = usuario.rol.nombre_rol
    negocio = usuario if rol == "Dueño" else usuario.owner_id

    if rol in ["Dueño", "Administrador"]:
        return Cliente.activos.filter(owner=negocio)

    if rol == "Vendedor":
        return Cliente.activos.filter(owner=negocio)

    return Cliente.activos.none()



def queryset_servicios_por_rol(usuario):
    rol = usuario.rol.nombre_rol
    # todos  deben ven los servicios del negocio, no solo los que crearon
    if rol == "Dueño":
        return Servicio.activos.filter(owner=usuario)

    if rol == "Administrador":
        return Servicio.activos.filter(owner=usuario.owner_id)

    if rol == "Vendedor":
        return Servicio.activos.filter(owner=usuario.owner_id)

    return Servicio.activos.none()

def queryset_inventario_por_rol(usuario):
    if usuario.rol.nombre_rol == "Dueño":
        return Inventario.activos.filter(owner=usuario)
    else:
        return Inventario.activos.filter(owner=usuario.owner_id)

#Superusuario...
def solo_superusuario(view_func):
    def wrapper(request, *args, **kwargs):
        # Primero revisamos la sesión para rapidez
        rol = request.session.get("rol")
        usuario_id = request.session.get("idusuario")
        
        if not usuario_id or rol != "Superusuario":
            return redirect("usuario:iniciar_sesion")
        # if request.session.get("rol") != "Superusuario":
        #   return redirect("usuario:login")
        return view_func(request, *args, **kwargs)
    return wrapper

''' 
Nota:
Para que el decorador sea más robusto,
 es mejor verificar directamente si el usuario existe 
 en la base de datos y es superusuario, por si cambias 
 el rol en la BD mientras la sesión sigue abierta.
'''
