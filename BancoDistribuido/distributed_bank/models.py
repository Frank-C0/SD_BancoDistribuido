from djongo import models
import bcrypt

class Banco(models.Model):
    nombre_banco = models.CharField(max_length=255)
    pais = models.CharField(max_length=255)

class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def save(self, *args, **kwargs):
        # Hashea la contraseña antes de guardarla en la base de datos
        self.password = bcrypt.hashpw(self.password.encode('utf-8'), bcrypt.gensalt())
        super().save(*args, **kwargs)

class Cuenta(models.Model):
    id_banco = models.ForeignKey(Banco, on_delete=models.CASCADE)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    path_file = models.CharField(max_length=255)
    numCuenta = models.CharField(max_length=20)
    numCuentaCCI = models.CharField(max_length=30)

class Transaccion(models.Model):
    # Define los campos de la transacción según tus necesidades
    pass
