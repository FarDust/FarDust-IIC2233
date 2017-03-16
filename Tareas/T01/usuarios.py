# Usuarios v1.0.0

from abc import ABCMeta, abstractmethod


class Usuario(metaclass=ABCMeta):
    def __init__(self, dic):
        self.id = dic["id"]
        self.nombre = dic["nombre"]
        self.password = dic["contraseña"]
        self.recurso_id = dic["recurso_id"]

    @abstractmethod
    def crear_usuario(self, name, password):
        pass

    @abstractmethod
    def consulta_basica(self):
        pass

    @abstractmethod
    def consulta_avanzada(self):
        pass


class Sudo(Usuario):
    def __init__(self, dic):
        super().__init__(dic)
        pass

    def crear_usuario(self, name, password):
        pass

    def consulta_avanzada(self):
        pass

    def consulta_basica(self):
        pass


class Terreno(Usuario):
    def __init__(self, dic):
        super().__init__(dic)
        pass

    def crear_usuario(self, name, password):
        pass

    def consulta_avanzada(self):
        pass

    def consulta_basica(self):
        pass
