from django.urls import path
from .views import DetalleCuentaView, RealizarDepositoView

urlpatterns = [
    path('detalle_cuenta/<int:cuenta_id>/', DetalleCuentaView.as_view(), name='detalle_cuenta'),
    path('realizar_deposito/<int:cuenta_id>/', RealizarDepositoView.as_view(), name='realizar_deposito'),

]