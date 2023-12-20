
from django.db import models
from apps.Cliente.models import Cliente 
from apps.Banco.models import Banco  

class Cuenta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuenta = models.CharField(max_length=20, unique=True)
    numero_cuenta_interbancario = models.CharField(max_length=30, unique=True)
    fecha_apertura = models.DateField()
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.numero_cuenta} - {self.banco.nombre}'

    class Meta:
        verbose_name_plural = 'Cuentas'

class Transaccion(models.Model):
    cuenta_origen = models.ForeignKey(Cuenta, related_name='transacciones_origen', on_delete=models.CASCADE)
    cuenta_destino = models.ForeignKey(Cuenta, related_name='transacciones_destino', on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transacción de {self.cuenta_origen} a {self.cuenta_destino}'

    class Meta:
        ordering = ['-fecha']
        verbose_name_plural = 'Transacciones'