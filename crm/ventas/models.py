from django.db import models
from django.utils import timezone
from usuario.models import Usuario
from servicios.models import Servicio
from inventario.models import Inventario
from cliente.models import Cliente
from cobros.models import EstatusCobros

class ActivoManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

class EtapaVentas(models.Model):
    idetapa_ventas = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(max_length=45)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        managed = True
        db_table = 'etapa_ventas'
        ordering = ['orden']

    def __str__(self):
        return self.nombre_etapa

class Venta(models.Model):
    idventa = models.AutoField(primary_key=True)
    nombreventa = models.CharField(max_length=45)
    preciototal = models.DecimalField(max_digits=10, decimal_places=2)
    cfdi = models.CharField(max_length=100, unique=True, null=True,blank=True)
    comentarios = models.TextField(null=True,blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True,blank=True)
    estatus_cobro = models.ForeignKey(EstatusCobros, on_delete=models.PROTECT, db_column='estatus_cobro')
    oportunidad_venta = models.ForeignKey(
        'oportunidades.Oportunidad',
        on_delete=models.PROTECT,
        db_column='oportunidad_venta',
        null=True,
        blank=True
    )
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_registro')
    owner = models.ForeignKey(
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='ventas_del_negocio'
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT, 
        null=True,
        blank=True,
        db_column='cliente_id',    
        related_name='ventas'     
    )

    activos = ActivoManager()
    objects = models.Manager() 

    class Meta:
        managed = False
        db_table = 'ventas'
    
    def eliminar_logico(self):
        if self.activo:  
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"({self.nombreventa}) - ${self.preciototal} "
    
class VentaDetalle(models.Model):
    iddetalle_venta = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    venta_id = models.ForeignKey(
        Venta,
        on_delete=models.CASCADE,
        null=True,
        db_column='venta_id',
        related_name='detalles'
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.PROTECT,
        null=True, 
        blank= True,
        db_column='servicio_id',
        related_name='detalles_servicio'
    )
    inventario = models.ForeignKey(
        Inventario,
        on_delete=models.PROTECT,
        null=True,
        blank= True,
        db_column='inventario_id',
        related_name='detalles_inventario'
    )
    activo=models.BooleanField(default=True)

    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'detalle_venta'
    
    def __str__(self):
        if self.servicio:
            item = self.servicio.nombre
        elif self.inventario:
            item = self.inventario.nombrearticulo
        else:
            item = "Concepto no especificado"
        return f"{self.cantidad}x {item} en Venta #{self.venta_id}"