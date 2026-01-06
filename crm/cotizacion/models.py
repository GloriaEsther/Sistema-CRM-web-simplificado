from django.db import models
from servicios.models import Servicio
from cliente.models import Cliente
from usuario.models import Usuario
#para eliminacion logica....
class ActivoManager(models.Manager):
    """Devuelve solo los registros activos (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)
      
class Cotizacion(models.Model):
    idcotizacion = models.AutoField(primary_key=True)
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT
    )
    owner = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='cotizaciones_del_negocio'
    )
    usuario_registro = models.ForeignKey(
         Usuario,
         on_delete =models.PROTECT, db_column='usuario_registro'
    )
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    activo=models.BooleanField(default=True)
    
    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'cotizacion'

    def __str__(self):
        return f"Cotización #{self.idcotizacion} - {self.cliente}"

class CotizacionDetalle(models.Model):
    iddetallecotizacion = models.AutoField(primary_key=True)
    cotizacion = models.ForeignKey(
        Cotizacion,
        related_name='detalles',
        on_delete=models.CASCADE
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT
    )
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    activo=models.BooleanField(default=True)

    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'cotizacion_detalle'
        

    def __str__(self):
            return f"Cotización #{self.iddetallecotizacion} - {self.cotizacion}"
