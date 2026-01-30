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
from proveedor.models import Proveedor
from ventas.models import Venta
from cotizacion.models import Cotizacion
import pandas as pd
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

def queryset_usuarios_segun_rol(usuario,owner):#es un filtro en las busquedas de usuario al crear oportunidades
    if not owner:
        return Usuario.activos.none()
    rol = usuario.rol.nombre_rol
    if rol in ["Dueño", "Administrador","Superusuario","Consultor"]:
        return Usuario.activos.filter(
            Q(idusuario = owner.idusuario) |
            Q(owner_id = owner.idusuario)
        )

    if rol == "Vendedor":
        return Usuario.activos.filter(idusuario=usuario.idusuario)

    return Usuario.activos.none()

def queryset_clientes_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol
    if rol == "Superusuario":
        return Cliente.todos.filter(owner = owner)
    
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Cliente.activos.filter(owner = owner)

    if rol == "Vendedor":
        return Cliente.activos.filter(owner = owner)

    return Cliente.activos.none()

def clientes_para_oportunidad(usuario, owner):
    if not owner:
        return Cliente.activos.none()
    rol = usuario.rol.nombre_rol

    if rol in ["Dueño", "Administrador","Superusuario","Consultor"]:
        return Cliente.activos.filter(owner = owner)

    if rol == "Vendedor":
        return Cliente.activos.filter(owner = owner)
    return Cliente.activos.filter(owner=owner)


def queryset_servicios_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol
    if rol == "Superusuario":
        return Servicio.todos.filter(owner = owner)
    
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Servicio.activos.filter(owner = owner)

    if rol == "Vendedor":
        return Servicio.activos.filter(owner = owner)

    return Servicio.activos.none()

def queryset_inventario_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol
    if rol == "Superusuario":
        return Inventario.todos.filter(owner = owner)
    
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Inventario.activos.filter(owner = owner)

    if rol == "Vendedor":
        return Inventario.activos.filter(owner = owner)

    return Inventario.activos.none()

#Superusuario...
def solo_superusuario(view_func):
    def wrapper(request, *args, **kwargs):
        rol = request.session.get("rol")
        usuario_id = request.session.get("idusuario")
        if not usuario_id or rol != "Superusuario":
            return redirect("usuario:iniciar_sesion")
        return view_func(request, *args, **kwargs)
    return wrapper

def solo_supervisor(view_func):
    def _wrapped_view(request, *args, **kwargs):
        rol = request.session.get("rol")
        if rol not in ["Superusuario", "Consultor"]:
            messages.error(request, "No tienes permiso para acceder")
            return redirect("inicio")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def obtener_owner(request, usuario):
    rol = usuario.rol.nombre_rol

    if rol == "Superusuario" or rol == "Consultor":#
        owner_id = request.session.get("dueno_supervisado")
        if owner_id:
            return Usuario.activos.filter(idusuario=owner_id).first()
        return None

    if rol == "Dueño":
        return usuario

    return usuario.owner_id

def queryset_proveedores_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol
   
    if rol == "Superusuario":
        return Proveedor.todos.filter(owner=owner)
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Proveedor.activos.filter(owner=owner)
    if rol == "Vendedor":
        return Proveedor.activos.none()

    return Proveedor.todos.none()

#para importar cliente...
def limpiar_valor(valor):
    if pd.isna(valor) or str(valor).strip() == "":
        return None
    return str(valor).strip()

#ventas
def queryset_ventas_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol
    if rol == "Superusuario":
        return Venta.objects.filter(owner = owner)
    
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Venta.activos.filter(owner = owner)

    if rol == "Vendedor":
        return Venta.activos.filter(owner = owner)

    return Venta.activos.none()

def queryset_cotizaciones_por_rol(usuario,owner):
    rol = usuario.rol.nombre_rol

    if rol == "Superusuario":
        return Cotizacion.todos.filter(owner=owner)
    if rol in ["Dueño", "Administrador","Consultor"]:
        return Cotizacion.activos.filter(owner=owner)

    if rol == "Vendedor":
        return Cotizacion.activos.filter(owner=owner)

    return Cotizacion.todos.none()

def queryset_empleados_por_rol(usuario, owner):
    rol = usuario.rol.nombre_rol

    if not owner:
        return Usuario.activos.none()

    if rol == "Superusuario":
        return Usuario.todos.filter(
            owner_id=owner
        ).exclude(
            rol__nombre_rol="Dueño"
        )

    if rol in ["Dueño", "Administrador"]:#,"Consultor"
        return Usuario.activos.filter(
            owner_id=owner
        ).exclude(
            rol__nombre_rol="Dueño"
        )

    return Usuario.activos.none()

def obtener_usuario_perfil(request):
    usuario = Usuario.activos.get(
        idusuario=request.session.get("idusuario")
    )
    dueno_id = request.session.get("dueno_supervisado")
    if dueno_id:
        return Usuario.activos.filter(
            idusuario=dueno_id,
            rol__nombre_rol="Dueño"
        ).first()
    return usuario