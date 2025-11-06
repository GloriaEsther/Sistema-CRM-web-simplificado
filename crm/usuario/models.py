from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class ActivoManager(models.Manager):
    """Devuelve solo los registros activos de usuarios (no eliminados)"""
    def get_queryset(self):
        return super().get_queryset().filter(activo=True)
                            #02/11/25 y 03/11/25
class Usuario(models.Model):#te quedasta aqui en revisar y ponerle el modelo a los demas modulos para implementar la eliminacion logica desde un principio el archivo se llama:tejuroqueahorasisieslaversionfinaldelabd.sql
    ROLES = [
        ('Dueño', 'Dueño'),
        ('Administrador', 'Administrador'),
        ('Vendedor', 'Vendedor'),
    ]
    LOCAL_FIJO_OPCIONES = [
        ('Si', 'Si'),
        ('No', 'No'),
    ]

    idusuario = models.AutoField(primary_key=True)
    claveusuario = models.CharField(unique=True, max_length=10,blank=True)#se permite null para guardar al ultimo la clave ya que el modelo lo crea antes de guardarla
    nombre = models.CharField(max_length=45)
    apellidopaterno = models.CharField(max_length=45)
    apellidomaterno = models.CharField(max_length=45)
    numerotel = models.CharField(max_length=25)
    correo = models.CharField(unique=True, max_length=100)
    contrasena = models.CharField(max_length=255)
    rfc = models.CharField(max_length=13)
    direccion = models.CharField(max_length=255)
    curp = models.CharField(max_length=18)
    rol = models.CharField(max_length=13, choices=ROLES)
    local_Fijo = models.CharField(db_column='local_Fijo', max_length=2, choices=LOCAL_FIJO_OPCIONES, blank=True, null=True)
    
    fecha_registro = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    nss = models.CharField(max_length=11, blank=True, null=True)
   
    activo = models.BooleanField(default=True)
    fecha_eliminacion = models.DateTimeField(blank=True, null=True)

    activos = ActivoManager()
    todos = models.Manager()
    
    '''
    def save(self, *args, **kwargs):
        if not self.pk or 'pbkdf2_sha256$' not in self.contrasena:
            self.contrasena = make_password(self.contrasena)

        if not self.claveusuario:
           last_id = Usuario.objects.count() + 1
           self.claveusuario = f"USR{last_id:03d}"
        super().save(*args, **kwargs)
    '''
    def generar_clave(self):
        # Prefijo según rol
        prefijo = ''
        if self.rol=='Vendedor':#self.rol.lower() == 'Vendedor':
            prefijo = 'VEN'
        elif self.rol== 'Administrador':#self.rol.lower() == 'Administrador':
            prefijo = 'ADM'
        else:
            prefijo = 'Due'
        # Contar cuántos usuarios existen con ese prefijo
        cantidad = Usuario.todos.filter(claveusuario__startswith=prefijo).count() + 1
        return f"{prefijo}{cantidad:03d}"  # VEN001, VEN002, etc.

    def save(self, *args, **kwargs):
        # Hashea la contrasena si no lo esta
        if not self.contrasena.startswith('pbkdf2_sha256$'):
            self.contrasena = make_password(self.contrasena)

        # Crea claveusuario si no existe
        if not self.claveusuario:
            self.claveusuario = self.generar_clave()

        super().save(*args, **kwargs)

     
    class Meta:
        managed = False
        db_table = 'usuario'

    def eliminar_logico(self):
        if self.activo:  # evita volver a marcarlo si ya está eliminado
            self.activo = False
            self.fecha_eliminacion = timezone.now()
            self.save()

    def __str__(self):
        return f"{self.claveusuario} {self.nombre} {self.apellidopaterno} {self.apellidomaterno} {self.rol} {self.correo} {self.numerotel}{self.rfc} "
