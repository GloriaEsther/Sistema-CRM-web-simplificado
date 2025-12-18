from django.db import models
from usuario.models import Usuario
from django.utils import timezone

#para eliminacion logica....
class ActivoManager(models.Manager):
    """Devuelve solo los registros activos de usuarios (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)
    
# Create your models here.
class Proveedor(models.Model):
    idproveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150,verbose_name="Nombre Comercial")
    numero = models.CharField(max_length=10,blank=True,null=True,verbose_name="Teléfono")
    
     # Datos Fiscales (México SAT)
    razon_social = models.CharField(
        max_length=250, 
        verbose_name="Razón Social"
    )
    rfc_proveedor = models.CharField(
        max_length=13, 
        unique=True, 
        verbose_name="RFC"
    )
    codigo_postal = models.CharField(
        max_length=5, 
        verbose_name="Código Postal Fiscal"
    )

 # Control y Notas
    activo = models.BooleanField(
        default=True, 
        verbose_name="Estado Activo"
    )
    comentarios = models.TextField(blank=True,null=True)
    
    usuario_registro = models.ForeignKey(Usuario, on_delete=models.PROTECT, db_column='usuario_registro')
    owner = models.ForeignKey(#esto es para distinguir los clientes de cada negocio(como owner_id pero aplicado a clientes)
        Usuario,
        on_delete=models.PROTECT,
        db_column='owner_id',
        related_name='proveedores_del_negocio',
        null=True,
        blank=True
    )


    activos = ActivoManager()
    todos = models.Manager()

    class Meta:
        managed = False
        db_table = 'proveedor'
        #verbose_name = "Proveedor"
        #verbose_name_plural = "Proveedores"

    def __str__(self):
        return f"{self.nombre} ({self.rfc_proveedor})"
    
    def save(self, *args, **kwargs):
        # Forzar RFC a mayúsculas siempre antes de guardar
        if self.rfc_proveedor:
            self.rfc_proveedor = self.rfc_proveedor.upper()
        super(Proveedor, self).save(*args, **kwargs)