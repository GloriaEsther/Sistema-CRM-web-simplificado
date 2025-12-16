from django.db import models
from usuario.models import Usuario
from django.utils import timezone
#para eliminacion logica....
class ActivoManager(models.Manager):
    """Devuelve solo los registros activos de usuarios (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)

#Las siguientes 3 clases son otras tablas en la bd..
class TipoArticuloCat(models.Model):
    idtipo_articulo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'tipo_articulo_cat'

    def __str__(self):
        return self.nombre_tipo


class UnidadCat(models.Model):
    idunidad_cat = models.AutoField(primary_key=True)
    nombre_unidad = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'unidad_cat'

    def __str__(self):
        return self.nombre_unidad

class Proveedor(models.Model):
    idproveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45,blank=True,null=True)
    numero = models.CharField(max_length=10,blank=True,null=True)
    comentarios = models.TextField(blank=True,null=True)
    class Meta:
        managed = False
        db_table = 'proveedor'

    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    idinventario = models.AutoField(primary_key=True)
    nombrearticulo = models.CharField(max_length=45)
    descripcion = models.CharField(max_length=45, null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad_disponible = models.IntegerField(null=True, blank=True)
    comentarios = models.TextField(null=True, blank=True)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)
    #Claves foraneas
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_registro')
    owner = models.ForeignKey(#esto es para distinguir los clientes de cada negocio(como owner_id pero aplicado a clientes)
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='productos_del_negocio',
        null=True,
        blank=True
    )
    tipo= models.ForeignKey(TipoArticuloCat, on_delete=models.PROTECT, db_column='tipo',null=True,blank=True)
    unidad= models.ForeignKey(UnidadCat, on_delete=models.PROTECT, db_column='unidad',null=True,blank=True)
    proveedor=  models.ForeignKey(Proveedor, on_delete=models.PROTECT, db_column='proveedor',null=True,blank=True)
   
    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'inventario'

    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.nombrearticulo} - ${self.precio} {self.descripcion} {self.cantidad_disponible}"