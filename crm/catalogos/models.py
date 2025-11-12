from django.db import models

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


class RolUsuario(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'rol_usuario'

    def __str__(self):
        return self.nombre_rol


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

