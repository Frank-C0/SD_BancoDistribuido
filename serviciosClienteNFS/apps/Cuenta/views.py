from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Cuenta, Transaccion
from bson.decimal128 import Decimal128
from decimal import Decimal, InvalidOperation

class DetalleCuentaView(View):
    template_name = 'detalle_cuenta.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        return render(request, self.template_name, {'cuenta': cuenta})

class RealizarDepositoView(View):
    template_name = 'realizar_deposito.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        cuentas_destino = Cuenta.objects.exclude(id=cuenta_id)  # Excluye la cuenta actual como destinatario
        return render(request, self.template_name, {'cuenta': cuenta, 'cuentas_destino': cuentas_destino})

    def post(self, request, cuenta_id):
        monto_str = request.POST.get('monto')
        cuenta_destino_id = request.POST.get('cuenta_destino')

        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id)
        cuenta_destino = get_object_or_404(Cuenta, id=cuenta_destino_id)

        try:
            monto = (Decimal(monto_str))
        except InvalidOperation:
            mensaje = 'El monto proporcionado no es válido.'
            return render(request, self.template_name, {'cuenta': cuenta, 'cuentas_destino': Cuenta.objects.exclude(id=cuenta_id), 'mensaje': mensaje})
        # Lógica para procesar el depósito (guardar la transacción, actualizar el saldo, etc.)
        
        if monto and cuenta_destino:
            
            transaccion = Transaccion.objects.create(
                cuenta_origen=cuenta_origen,
                cuenta_destino=cuenta_destino,
                monto=monto
            )
            cuenta_origen.saldo = (cuenta_origen.saldo.to_decimal() - monto)
            cuenta_destino.saldo = (cuenta_destino.saldo.to_decimal() + monto)

            cuenta_origen.save()
            cuenta_destino.save()

            mensaje = f'Depósito de {monto} realizado a la cuenta {cuenta_destino.numero_cuenta} con éxito.'
        else:
            mensaje = 'Por favor, selecciona un destinatario y proporciona el monto del depósito.'

        return render(request, self.template_name, {'cuenta': cuenta_origen, 'cuentas_destino': Cuenta.objects.exclude(id=cuenta_id), 'mensaje': mensaje})