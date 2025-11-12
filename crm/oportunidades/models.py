from django.db import models
from usuario.models import Usuario
from cliente.models import Cliente
from ventas.models import Venta, EtapaVentas

class Oportunidad(models.Model):
    idoportunidad = models.AutoField(primary_key=True)
    nombreoportunidad = models.CharField(max_length=45)
    valor_estimado = models.DecimalField(max_digits=10, decimal_places=2)
    #Opcional
    fecha_cierre_estimada = models.DateTimeField(null=True)
    comentarios = models.TextField(null=True)
   #Sistema
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_eliminacion = models.DateTimeField(null=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
   #Claves Foraneas
    cliente_oportunidad = models.ForeignKey(Cliente, on_delete=models.PROTECT, db_column='cliente_oportunidad')
    etapa_ventas = models.ForeignKey(EtapaVentas, on_delete=models.PROTECT, db_column='etapa_ventas')
    usuario_responsable = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_responsable')

    class Meta:
        managed = False
        db_table = 'oportunidades'

    def __str__(self):
        return self.nombreoportunidad
