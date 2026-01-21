from django.db import models
from usuario.models import Usuario
from django.utils import timezone
#para eliminacion logica....
class ActivoManager(models.Manager):
    """Devuelve solo los registros activos (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

class EstadoClienteCat(models.Model):
    idestado_cliente = models.AutoField(primary_key=True)
    nombre_estado = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'estado_cliente_cat'

    def __str__(self):
        return self.nombre_estado


class FrecuenciaClienteCat(models.Model):
    idfrecuencia_cliente = models.AutoField(primary_key=True)
    nombre_frecuencia = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'frecuencia_cliente_cat'

    def __str__(self):
        return self.nombre_frecuencia

class Cliente(models.Model):
    idcliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellidopaterno = models.CharField(max_length=45, blank=True,null=True)
    apellidomaterno = models.CharField(max_length=45, blank=True,null=True)
    numerotelcli = models.CharField(max_length=10)
    #Opcionales
    correo = models.CharField(max_length=100, blank=True,null=True)
    direccion = models.CharField(max_length=255, blank=True,null=True)
    rfc = models.CharField(max_length=13,blank=True, null=True)
    fecha_nacimiento = models.DateTimeField(blank=True, null=True)
    fecha_ultimocontacto = models.DateTimeField(blank=True,null=True)
    comentarios = models.TextField(blank=True,null=True)
   
   #Sistema
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(null=True)
    
   #claves foraneas
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_registro')
    frecuencia_compra = models.ForeignKey(FrecuenciaClienteCat, on_delete=models.PROTECT, db_column='frecuencia_compra',null=True,blank=True)
    estado_cliente = models.ForeignKey(EstadoClienteCat, on_delete=models.PROTECT, db_column='estado_cliente',null=True,blank=True)
    owner = models.ForeignKey(#esto es para distinguir los clientes de cada negocio(como owner_id pero aplicado a clientes)
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='clientes_del_negocio',
        null=True,
        blank=True
    )
    
    activos = ActivoManager()
    todos = models.Manager()
    
    class Meta:
        managed = False#Django no aplicara cambios en las tablas aunque hagas migraciones cuando lo tienes en True si lo hace
        db_table = 'cliente'
    
    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.nombre} {self.apellidopaterno} {self.apellidomaterno}"