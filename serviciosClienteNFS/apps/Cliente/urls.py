# miapp/urls.py
from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("",RedirectView.as_view(url='login/',permanent=True)),
    # Otras rutas específicas de miapp
]
