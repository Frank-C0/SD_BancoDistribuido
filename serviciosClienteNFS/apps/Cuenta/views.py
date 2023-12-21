from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Cuenta, Transaccion
from bson.decimal128 import Decimal128
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import transaction

class DetalleCuentaView(View):
    template_name = 'detalle_cuenta.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        return render(request, self.template_name, {'cuenta': cuenta})

class RealizarTransferenciaInternaView(View):
    template_name = 'realizar_transferencia.html'

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
        # Lógica para procesar la Tranferencia (guardar la transacción, actualizar el saldo, etc.)
        
        if monto and cuenta_destino:
            
            transaccion = Transaccion.objects.create(
                cuenta_origen=cuenta_origen,
                cuenta_destino=cuenta_destino,
                monto=monto,
                tipo='TRANSFERENCIA'
                # fecha=datetime.now()
            )
            cuenta_origen.saldo = (cuenta_origen.saldo.to_decimal() - monto)
            cuenta_destino.saldo = (cuenta_destino.saldo.to_decimal() + monto)

            cuenta_origen.save()
            cuenta_destino.save()

            mensaje = f'Tranferencia de {monto} realizado a la cuenta {cuenta_destino.numero_cuenta} con éxito.'
        else:
            mensaje = 'Por favor, selecciona un destinatario y proporciona el monto la Tranferencia.'

        return render(request, self.template_name, {'cuenta': cuenta_origen, 'cuentas_destino': Cuenta.objects.exclude(id=cuenta_id), 'mensaje': mensaje})

class RealizarTransferenciaInterbancariaView(View):
    template_name = 'realizar_transferencia_interbancaria.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        return render(request, self.template_name, {'cuenta': cuenta})

    def post(self, request, cuenta_id):
        monto_str = request.POST.get('monto')
        cuenta_destino = request.POST.get('cuenta_destino_numero')
        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id)

        try:
            monto = Decimal(monto_str)
        except InvalidOperation:
            mensaje = 'El monto proporcionado no es válido.'
            return render(request, self.template_name, {'cuenta': cuenta_origen, 'mensaje': mensaje})
            
        # Puedes crear una instancia de Transaccion para registrar la operación
        if monto and cuenta_destino:
            transaccion = Transaccion.objects.create(
                cuenta_origen=cuenta_origen,
                cuenta_destino=cuenta_destino,
                monto=monto,
                tipo='TRANSFERENCIA INTERBANCARIA'
                # fecha=datetime.now()
            )
            cuenta_origen.saldo = (cuenta_origen.saldo.to_decimal() - monto)
            cuenta_destino.saldo = (cuenta_destino.saldo.to_decimal() + monto)

            cuenta_origen.save()
            cuenta_destino.save()

            mensaje = f'Tranferencia de {monto} realizado a la cuenta {cuenta_destino.numero_cuenta} con éxito.'
        else:
            mensaje = 'Por favor, selecciona un destinatario y proporciona el monto la Tranferencia.'


        # Puedes implementar la lógica para comunicarte con el sistema de otro banco y procesar la transferencia

        mensaje = f'Transferencia de {monto} a la cuenta {cuenta_destino_numero} en el banco {banco_destino} realizada con éxito.'
        return render(request, self.template_name, {'cuenta': cuenta_origen, 'mensaje': mensaje})


class RealizarDepositoView(View):
    template_name = 'realizar_deposito.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        return render(request, self.template_name, {'cuenta': cuenta})

    def post(self, request, cuenta_id):
        monto_str = request.POST.get('monto')

        cuenta_destino = get_object_or_404(Cuenta, id=cuenta_id)

        try:
            monto = Decimal(monto_str)
        except InvalidOperation:
            mensaje = 'El monto proporcionado no es válido.'
            return render(request, self.template_name, {'cuenta': cuenta_destino, 'mensaje': mensaje})

        # Lógica para procesar el depósito (guardar la transacción, actualizar el saldo, etc.)
        if monto:
            transaccion = Transaccion.objects.create(
                cuenta_destino=cuenta_destino,
                monto=monto,
                tipo='DEPOSITO'
                # fecha=datetime.now()
            )
            cuenta_destino.saldo = cuenta_destino.saldo.to_decimal() + monto
            cuenta_destino.save()

            mensaje = f'Depósito de {monto} realizado con éxito.'
        else:
            mensaje = 'Por favor, proporciona un monto válido para el depósito.'

        return render(request, self.template_name, {'cuenta': cuenta_destino, 'mensaje': mensaje})


class RealizarRetiroView(View):
    template_name = 'realizar_retiro.html'

    def get(self, request, cuenta_id):
        cuenta = get_object_or_404(Cuenta, id=cuenta_id)
        return render(request, self.template_name, {'cuenta': cuenta})

    def post(self, request, cuenta_id):
        monto_str = request.POST.get('monto')

        cuenta_origen = get_object_or_404(Cuenta, id=cuenta_id)

        try:
            monto = Decimal(monto_str)
        except InvalidOperation:
            mensaje = 'El monto proporcionado no es válido.'
            return render(request, self.template_name, {'cuenta': cuenta_origen, 'mensaje': mensaje})

        # Lógica para procesar el retiro (guardar la transacción, actualizar el saldo, etc.)
        if monto and cuenta_origen.saldo.to_decimal() >= monto:
            transaccion = Transaccion.objects.create(
                cuenta_origen=cuenta_origen,
                monto=monto,
                tipo='RETIRO'
                # fecha=datetime.now()
            )
            cuenta_origen.saldo = cuenta_origen.saldo.to_decimal() - monto
            cuenta_origen.save()

            mensaje = f'Retiro de {monto} realizado con éxito.'
        else:
            mensaje = 'Fondos insuficientes o monto no válido para el retiro.'

        return render(request, self.template_name, {'cuenta': cuenta_origen, 'mensaje': mensaje})