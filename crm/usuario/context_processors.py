from usuario.models import Usuario
from usuario.models import PreferenciaUsuario

def usuario_actual(request):#te quedaste en resolver lo del logo, lo demas funciona, lo unico que debes haceres
    #encargarte de terminar la documentacion y la liberacion de residencia a tiempo
    #ademas tienes junta a las 10 
    usuario = None
    preferencias = None

    usuario_id = request.session.get("idusuario")

    if usuario_id:
        usuario = Usuario.activos.filter(
            idusuario=usuario_id
        ).select_related("rol").first()

        if usuario:
            dueno = (
                usuario
                if usuario.rol.nombre_rol == "Dueño"
                else usuario.owner_id
            )
            preferencias = PreferenciaUsuario.objects.filter(
                usuario=dueno
            ).first()

    return {
        "usuario": usuario,
        "preferencias": preferencias
    }

