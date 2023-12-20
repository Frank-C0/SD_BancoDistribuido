from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import ListView
from apps.Cuenta.models import Cuenta

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)
        # a = authenticate()
        user = authenticate(request, email=email, password=password)
        print("paso")    
        print(user)
        if user is not None:
            login(request, user)
            print(request, 'Inicio de sesión exitoso.')
            return redirect('lista_cuentas', cliente_id=user.id)
        else:
            print(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'login.html')



class ListaCuentasView(ListView):
    model = Cuenta
    template_name = 'lista_cuentas.html'
    context_object_name = 'cuentas'

    def get_queryset(self):
        cliente_id = self.kwargs['cliente_id']
        return Cuenta.objects.filter(cliente__id=cliente_id)


