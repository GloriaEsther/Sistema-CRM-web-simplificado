from django.db import models
from oportunidades.models import Oportunidad
class EtapaVentas(models.Model):
    idetapa_ventas = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'etapa_ventas'

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
    #Opcional
    cfdi = models.CharField(max_length=100, unique=True, null=True)
    comentarios = models.TextField(null=True)
   
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True)
   #Clave Foranea
    estatus_cobro = models.ForeignKey(EstatusCobros, on_delete=models.PROTECT, db_column='estatus_cobro')
   #su relacion 1:1 con Oportunidad
    oportunidad_venta = models.ForeignKey(Oportunidad,on_delete=models.PROTECT,db_column='oportunidades')
    class Meta:
        managed = False
        db_table = 'ventas'

    def __str__(self):
        return f"{self.nombreventa} ({self.claveventa})"


