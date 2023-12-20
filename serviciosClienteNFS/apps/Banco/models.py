from django.db import models

class Banco(models.Model):
    PAIS_CHOICES = [
        ('PE', 'Perú'),
        ('CN', 'China'),
        ('FR', 'Francia'),
    ]

    nombre = models.CharField(max_length=100)
    pais = models.CharField(max_length=2, choices=PAIS_CHOICES)

    def __str__(self):
        return self.nombre
    
    class Meta:
            verbose_name_plural = 'Bancos'
