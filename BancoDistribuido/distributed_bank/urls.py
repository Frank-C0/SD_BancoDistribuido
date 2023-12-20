
from django.urls import path
from .views import login_cliente, dashboard, logout_view

urlpatterns = [
    path('login/', login_cliente, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', logout_view, name='logout'),
    # Agrega otras URL según sea necesario
]