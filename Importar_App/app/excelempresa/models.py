from django.db import models

from decimal import Decimal

import datetime


# Create your models here.
class Restaurante(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    razon_social = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    cuenta_bancaria = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    nif_cif = models.CharField(max_length=10, blank=True, null=True)
    poblacion = models.CharField(max_length=20, blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    
    precio_base_envio = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    cantidad_pedidos = models.IntegerField(blank=True, null=True)
    cantidad_recaudada = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    gastos_envio = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    cantidad_transferir = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    importe_iva = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    importe_sin_iva = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    tarifa_mensual = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return self.id + ": " + self.nombre

    def porcentaje_gastos(self):
        p = self.gastos_envio / self.cantidad_recaudada
        return "{:.2%}".format(p)


class Repartidor(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=9, blank=True, null=True)
    cuenta_bancaria = models.CharField(max_length=30, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=20, blank=True, null=True)
    poblacion = models.CharField(max_length=20, blank=True, null=True)
    codigo_postal = models.CharField(max_length=5, blank=True, null=True)
    nif_cif = models.CharField(max_length=10, blank=True, null=True)

    cantidad_repartos = models.IntegerField(blank=True, null=True)
    cantidad_transferir = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    importe_iva = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    importe_sin_iva = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    precio_base = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    precio_extra = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "repartidores"

    def __str__(self):
        return self.id + ": " + self.nombre


class Pedido(models.Model):
    numero = models.CharField(max_length=7, primary_key=True)
    task_id = models.CharField(max_length=9, blank=True, null=True)
    estado = models.CharField(max_length=20, blank=True, null=True)
    subtotal_pedido = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    tipo = models.CharField(max_length=20, blank=True, null=True)
    total_pedido = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha = models.DateField(default = datetime.date.today)

    restaurante = models.ForeignKey(Restaurante, blank=True, null=True, on_delete=models.CASCADE)
    repartidor = models.ForeignKey(Repartidor, blank=True, null=True, on_delete=models.CASCADE)

    # task_id = models.ForeignKey('Envio', blank=True, null=True, on_delete=models.CASCADE, related_name='envio_assigned_to_pedido')

    def __str__(self):
        return "Pedido N° " + self.numero

    def porcentaje(self):
        try:
            p = 1 - (self.total_pedido / self.subtotal_pedido)
        except:
            p = 0
        return "{}%".format(round(p * 100,2))


class Envio(models.Model):
    # task_id = models.CharField(max_length=9, primary_key=True)
    coste_envio = models.DecimalField(max_digits=8, decimal_places=2)
    distancia_metros = models.IntegerField()
    fecha = models.DateField(default=datetime.date.today)

    repartidor = models.ForeignKey(Repartidor, blank=True, null=True, on_delete=models.CASCADE)
    pedido = models.ForeignKey(Pedido, blank=True, null=True, on_delete=models.CASCADE)

    def distancia_km(self):
        return self.distancia_metros / 1000

    def iva(self):
        return self.coste_envio * 21 / 100

    def importe_sin_iva(self):
        return self.coste_envio - self.iva()


class Constants(models.Model):
    id = models.IntegerField(default=1, primary_key=True)
    fecha_inicio = models.DateField(default=datetime.date.today)
    fecha_fin = models.DateField(default=datetime.date.today)