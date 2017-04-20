__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime

"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def log(funcion):
    def _log(*args):
        return
    return _log


def verificar_transferencia(funcion):
    def _verificar(self, origen, destino, monto, clave):
        verificar_existencia(self, origen)
        verificar_existencia(self, destino)
        if self.cuentas[origen].saldo < monto:
            raise AssertionError("No hay dinero suficiente para la transferencia {}->{}".format(origen, destino))
        elif self.cuentas[origen].clave == clave:
            raise AssertionError("La clave de transferencia es invalida")
        else:
            return funcion

    return _verificar


def verificar_inversion(funcion):
    def _verificar_inversion(self, cuenta, monto, clave):
        verificar_existencia(self, cuenta)
        if self.cuentas[cuenta].saldo < monto:
            raise AssertionError("Saldo insuficiente")
        elif self.cuentas[cuenta].clave != clave:
            raise AssertionError("Clave de cuenta invalida")
        elif self.cuentas[cuenta].inversiones + monto > 10000000:
            raise AssertionError("Transaccion prohibida, monto maximo se exedera")
        else:
            return funcion

    return _verificar_inversion


def verificar_cuenta(funcion):
    def _verificar_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        numeros_cuentas = [cuenta.numero for cuenta in self.cuentas]
        try:
            if numero in numeros_cuentas:
                raise AssertionError("Numero de cuenta ya existente")
        except AssertionError:
            while numero in numeros_cuentas:
                numero = random.randint(0, max(numeros_cuentas) + 1)
        if len([filter(lambda x: x == "-", rut)]) != 1:
            raise AssertionError("El rut contiene mas de un guion")
        elif not "".join(filter(lambda x: x != "-", rut)).isnumeric():
            raise AssertionError("El rut contiene caracteres no validos")
        elif rut[-1].isdigit() and len(rut[rut.find("-") + 1:]) != 1:
            raise AssertionError("El rut contiene un digito verificador no valido")
        elif not rut[-1].isdigit():
            raise AssertionError("El rut no contiene digito verificador")
        elif not (clave.isnumeric()) and len(clave) != 4:
            raise AssertionError("La clave ingresada es invalida")
        else:
            return funcion

    return _verificar_cuenta



def verificar_saldo(funcion):
    def _verificar_saldo(self, numero_cuenta):
        verificar_existencia(self, numero_cuenta)
        if funcion(self, numero_cuenta) > self.cuentas[numero_cuenta].saldo:
            raise AssertionError("El saldo no corresponde a la cuenta")
        else:
            return funcion

    return _verificar_saldo


def verificar_existencia(self, numero_cuenta):
    try:
        self.cuentas[numero_cuenta]
    except KeyError:
        raise AssertionError("La cuenta {} no existe".format(numero_cuenta))


"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""


class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas 
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las 
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    try:
        bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())
    except AssertionError as err:
        print("ERROR:", err)
    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """

    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
