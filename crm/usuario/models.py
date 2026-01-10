from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.conf import settings

class ActivoManager(models.Manager):
    """Devuelve solo los registros activos de usuarios (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)


class PreferenciaUsuario(models.Model):
    usuario = models.OneToOneField("usuario.Usuario", on_delete=models.CASCADE)

    color_primario = models.CharField(max_length=20, default="#0d6efd")
    color_secundario = models.CharField(max_length=20, default="#6c757d")
    color_fondo = models.CharField(max_length=20, default="#ffffff")

    logo = models.ImageField(upload_to="logos/", null=True, blank=True)

    def __str__(self):
        return f"Preferencias de {self.usuario.nombre}"
    
class RolUsuario(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'rol_usuario'

    def __str__(self):
        return self.nombre_rol


class Usuario(models.Model):
    LOCAL_FIJO_OPCIONES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]

    idusuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellidopaterno = models.CharField(max_length=45)
    apellidomaterno = models.CharField(max_length=45,blank=True,null=True)
    numerotel = models.CharField(max_length=10,blank=True,null=True)
    correo = models.CharField(unique=True, max_length=100)
    contrasena = models.CharField(max_length=255)
    rol = models.ForeignKey(RolUsuario, on_delete=models.SET_DEFAULT, default=1,db_column='rol')
    rfc = models.CharField(max_length=13, blank=True, null=True,unique=True)
    local_Fijo = models.CharField(db_column='local_Fijo', max_length=2, choices=LOCAL_FIJO_OPCIONES, blank=True, null=True)
    nombre_negocio = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)
    owner_id = models.ForeignKey(#quien registro a quien antes usuario_registro
        'self',
        on_delete=models.SET_NULL,
        null=True,#False
        blank= True,
        db_column='owner_id'
    )
    activos = ActivoManager()
    todos = models.Manager()
    
    class Meta:
        managed = False
        db_table = 'usuario'

    def save(self, *args, **kwargs):
        # Hashea la contrasena si no lo esta
        if not self.contrasena.startswith('pbkdf2_sha256$'):
            self.contrasena = make_password(self.contrasena)
        return  super().save(*args, **kwargs)

    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
     return f"{self.nombre} {self.apellidopaterno} {self.apellidomaterno}".strip()