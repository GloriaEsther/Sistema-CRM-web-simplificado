from usuario.models import Usuario
from usuario.models import PreferenciaUsuario

def usuario_actual(request):
    usuario = None
    preferencias = None

    usuario_id = request.session.get("idusuario")

    if usuario_id:
        usuario = Usuario.activos.filter(
            idusuario=usuario_id
        ).select_related("rol").first()

        if usuario:
            preferencias = PreferenciaUsuario.objects.filter(
                usuario=usuario
            ).first()

    return {
        "usuario": usuario,
        "preferencias": preferencias
    }
