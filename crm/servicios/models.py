from django.db import models
from usuario.models import Usuario
from django.utils import timezone

#para eliminacion logica....
class ActivoManager(models.Manager):
    """Devuelve solo los registros activos de usuarios (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)
    
class Servicio(models.Model):
    idservicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    descripcion = models.TextField(null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_registro')#Todo registro fue hecho por un usuario(registroa quien registro que)
    owner = models.ForeignKey(#esto es para distinguir los servicios de cada negocio(como owner_id pero aplicado a Servicios)
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='servicios_del_negocio',#Todo servicio debe pertenecer a un negocio
        null=False,# null=True,
        blank=True
    )
    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'servicio'
    
    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.nombre} - ${self.precio} {self.descripcion}"#self.nombre