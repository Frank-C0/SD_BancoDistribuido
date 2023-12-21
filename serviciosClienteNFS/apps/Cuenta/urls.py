from django.urls import path
from .views import DetalleCuentaView, RealizarTransferenciaInternaView, RealizarDepositoView, RealizarRetiroView, RealizarTransferenciaInterbancariaView

urlpatterns = [
    path('detalle_cuenta/<int:cuenta_id>/', DetalleCuentaView.as_view(), name='detalle_cuenta'),
    path('realizar_transferencia/<int:cuenta_id>/', RealizarTransferenciaInternaView.as_view(), name='realizar_transferencia'),
    path('realizar_retiro/<int:cuenta_id>/', RealizarRetiroView.as_view(), name='realizar_retiro'),
    path('realizar_deposito/<int:cuenta_id>/', RealizarDepositoView.as_view(), name='realizar_deposito'),
    path('realizar_transferencia_interbancaria/<int:cuenta_id>/', RealizarTransferenciaInterbancariaView.as_view(), name='realizar_transferencia_interbancaria'),

]