# miapp/urls.py
from django.urls import path
from . import views
from django.views.generic import RedirectView
from .views import ListaCuentasView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("",RedirectView.as_view(url='login/',permanent=True)),
    path('cliente/<int:cliente_id>/cuentas/', ListaCuentasView.as_view(), name='lista_cuentas'),

    
    # Otras rutas específicas de miapp
]
