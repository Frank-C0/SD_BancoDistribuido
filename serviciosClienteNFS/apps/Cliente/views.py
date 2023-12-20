from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

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
            return redirect('/admin')#/home
        else:
            print(request, 'Credenciales inválidas. Inténtalo de nuevo.')

    return render(request, 'login.html')

