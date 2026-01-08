from django.db import models
from django.utils import timezone

class ActivoManager(models.Manager):
    """Devuelve solo los registros activos (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

class EtapaVentas(models.Model):
    idetapa_ventas = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(max_length=45)
    orden = models.PositiveIntegerField(default=1)

    class Meta:
        managed = True#False 
        db_table = 'etapa_ventas'
        ordering = ['orden']

    def __str__(self):
        return self.nombre_etapa

class EstatusCobros(models.Model):
    idestatus_cobros = models.AutoField(primary_key=True)
    nombre_estatus_cobro = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estatus_cobros'

    def __str__(self):
        return self.nombre_estatus_cobro
    
class Venta(models.Model):

    idventa = models.AutoField(primary_key=True)
    claveventa = models.CharField(max_length=10, unique=True)
    nombreventa = models.CharField(max_length=45)
    preciototal = models.DecimalField(max_digits=10, decimal_places=2)
    cfdi = models.CharField(max_length=100, unique=True, null=True,blank=True)
    comentarios = models.TextField(null=True,blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True,blank=True)
    estatus_cobro = models.ForeignKey(EstatusCobros, on_delete=models.PROTECT, db_column='estatus_cobro')
   #su relacion 1:1 con Oportunidad
    oportunidad_venta = models.ForeignKey('oportunidades.Oportunidad',on_delete=models.PROTECT,db_column='oportunidad_venta')
    
    activos = ActivoManager()
    #todos = models.Manager()
    objects = models.Manager() 

    def save(self, *args, **kwargs):
        if not self.claveventa:
            ultimo = Venta.objects.order_by('-idventa').first()
            next_id = ultimo.idventa + 1 if ultimo else 1
            self.claveventa = f"VTA{next_id:07d}"
        super().save(*args, **kwargs)

    class Meta:
        managed = False
        db_table = 'ventas'
    
    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.nombreventa} ({self.claveventa}) {self.preciototal} {self.comentarios} {self.oportunidad_venta}"