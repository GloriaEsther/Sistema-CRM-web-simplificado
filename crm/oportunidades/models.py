from django.db import models
from usuario.models import Usuario
from cliente.models import Cliente
from django.db import models
from django.utils import timezone

class ActivoManager(models.Manager):
    """Devuelve solo los registros activos(no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

class Oportunidad(models.Model):
    idoportunidad = models.AutoField(primary_key=True)
    nombreoportunidad = models.CharField(max_length=45)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_cierre_estimada = models.DateTimeField()
    comentarios = models.TextField(null=True, blank=True)
   
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   
    cliente_oportunidad = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='cliente_oportunidad')
    etapa_ventas = models.ForeignKey('ventas.EtapaVentas', on_delete=models.PROTECT, db_column='etapa_ventas')
    usuario_responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, related_name="oportunidades_asignadas_por",db_column='usuario_responsable')
    creado_por = models.ForeignKey(#quien registro que ahora es dueno, a futuro un nuevo empleado del dueno
        Usuario,
        on_delete=models.PROTECT,
        related_name="op_creada_por",
        null=False,
        db_column='creado_por'
    )
    negocio_oportunidad = models.ForeignKey(#negocio al que le pertenece oportunidad antes owner_id
        Usuario,
        on_delete=models.CASCADE,
        related_name="op_negocio",
        null=False,
        db_column='negocio_oportunidad'
    )
    activos = ActivoManager()
    todos = models.Manager()
    objects = models.Manager()

    class Meta:
        managed = False
        db_table = 'oportunidades'

    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def mismos_usuarios_de_mi_negocio(self):
     return Usuario.activos.filter(owner_id=self.owner_id)

    def __str__(self): 
        return f"{self.nombreoportunidad} {self.valor_estimado} {self.fecha_cierre_estimada} {self.etapa_ventas} {self.comentarios} {self.cliente_oportunidad} (Responsable: {self.usuario_responsable.nombre})"#{self.usuario_responsable.nombre}
