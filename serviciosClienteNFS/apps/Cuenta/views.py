import os
import simplejson as json
from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Cuenta, Transaccion
from bson.decimal128 import Decimal128
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import transaction
from django.forms import model_to_dict
import Pyro4
import time

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

    @transaction.atomic
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

    @transaction.atomic
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
        if monto and cuenta_destino and cuenta_origen.saldo.to_decimal()>=monto:
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

    @transaction.atomic
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

    @transaction.atomic
    def post(self, request, cuenta_id):

        print("post retirar")
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
            

            actualizar_archivo_json(cuenta_origen, None, monto, transaccion)
            cuenta_origen.save()
            print("guardado")

            
            mensaje = f'Retiro de {monto} realizado con éxito.'
        else:
            mensaje = 'Fondos insuficientes o monto no válido para el retiro.'

        return render(request, self.template_name, {'cuenta': cuenta_origen, 'mensaje': mensaje})


def request_cs(server):
    return server.request_cs()

def release_cs(server):
    return server.release_cs()

def can_enter_cs(server):
    return server.can_enter_cs()


def actualizar_archivo_json(cuenta_origen, cuenta_destino_numero, monto, transaccion):
    print("actualizar_archivo_json")

    ruta_archivo_json = f'/home/ubuntu/Bancos/serviciosClienteNFS/apps/Cuenta/CuentasArchivos/{cuenta_origen.numero_cuenta}_transacciones.json'


    server_uri = "PYRO:central_server@localhost:50000"

    with Pyro4.Proxy(server_uri) as central_server:
        

       
        
        request_cs(central_server)
        while not can_enter_cs(central_server):
            time.sleep(1)

        print(f"está en la sección crítica.")
        time.sleep(10)  # Simulando el tiempo en la sección crítica

        
        # Crea o carga el diccionario desde el archivo JSON
        if os.path.exists(ruta_archivo_json):
            with open(ruta_archivo_json, 'r') as archivo_json:
                datos = json.load(archivo_json)
        else:
            datos = {'id_cliente':cuenta_origen.cliente.id ,'cuenta': cuenta_origen.numero_cuenta, 'transacciones': []}

        # Agrega la nueva transacción al diccionario
        datos['transacciones'].append(model_to_dict(transaccion))   

        # Guarda el diccionario actualizado en el archivo JSON
        with open(ruta_archivo_json, 'w') as archivo_json:
            json.dump(json.loads(json.dumps(datos, use_decimal=True)), archivo_json)


        release_cs(central_server)
        print(f"salió de la sección crítica.")
        # time.sleep(2)  # Espera antes de intentar ingresar nuevamente

