from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required as dj_login_required
from django.contrib.auth import logout
from usuario.models import Usuario,RolUsuario
from django.db.models import Q

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

    if rol =="Dueño":
        return Usuario.activos.filter(Q(idusuario=usuario.idusuario) | Q(owner_id=usuario.idusuario))
    if rol =="Administrador":
        return Usuario.activos.filter(Q(idusuario=usuario.idusuario) | Q(owner_id=usuario.owner_id))

    if rol == "Vendedor":
        rol_vendedor = RolUsuario.objects.filter(nombre_rol__iexact="Vendedor").first()
        return Usuario.activos.filter(rol=rol_vendedor,owner_id=usuario.owner_id)

    return Usuario.activos.none()
