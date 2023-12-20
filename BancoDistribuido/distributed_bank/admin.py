# mi_app/admin.py

from django.contrib import admin
from .models import Banco, Cliente, Cuenta, Transaccion

admin.site.register(Banco)
admin.site.register(Cliente)
admin.site.register(Cuenta)
admin.site.register(Transaccion)
