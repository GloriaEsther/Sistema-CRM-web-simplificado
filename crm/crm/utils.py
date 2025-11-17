from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required as dj_login_required
from django.contrib.auth import logout
def require_roles(allowed_roles):
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
                return redirect('usuario:iniciar_sesion')  #('usuario:inicio') #si funciona pero es molesto sin un cerrar sesion
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator
