from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Cliente

class ClienteLoginForm(AuthenticationForm):
    cliente = forms.CharField(max_length=100, label='Nombre de Cliente')

    def clean(self):
        cleaned_data = super().clean()
        cliente = cleaned_data.get('cliente')
        if not Cliente.objects.filter(nombre_cliente=cliente).exists():
            raise forms.ValidationError('Cliente no encontrado.')
