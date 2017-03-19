# Entidades v1.0.0

from abc import ABCMeta, abstractmethod


class Entidades(metadata=ABCMeta):
    def __init__(self, nombre):
        self.nombre = nombre
        self.usuario = None


class ANAF(Entidades):
    def __init__(self):
        self.empleados = []
        pass


class Persona(Entidades):
    def __init__(self):
        pass


class Empleado(Persona):
    def __init__(self):
        pass


class Piloto(Persona):
    def __init__(self):
        self.aeronave = None
        pass


class Jefe(Persona):
    def __init__(self):
        pass
