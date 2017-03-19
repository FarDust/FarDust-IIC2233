# Usuarios v1.0.0

from abc import ABCMeta, abstractmethod
from leer import Users, Meteorology, Fire, Resources


class Usuario(metaclass=ABCMeta):
    def __init__(self, dic):
        self.id = dic["id"]
        self.nombre = dic["nombre"]
        self.password = dic["contraseña"]
        self.recurso_id = dic["recurso_id"]

    @abstractmethod
    def consulta_basica(self):
        pass

    @abstractmethod
    def consulta_avanzada(self):
        pass


# Corresponde al ususario ANAF
class Anaf(Usuario):
    def __init__(self, dic):
        super().__init__(dic)
        pass

    def crear_usuario(self, name, password, recurso = ""):
        lexicon = Users().diccionario
        id = 0
        while (True):
            if not (str(id) in Users().leer.keys()):
                id = str(id)
                break
            else:
                id += 1
        (lexicon["id"], lexicon["nombre"], lexicon["contraseña"], lexicon["recurso_id"]) = (id, name, password, recurso)
        Users().escribir(lexicon)
        pass

    def agregar_pronostico(self, lexicon):
        # id, fecha_inicio, fecha_termino, tipo, valor, lat, lon, radio
        Meteorology().escribir(lexicon)

    def agregar_incendio(self, lexicon):
        Fire().escribir(lexicon)
        pass

    def consulta_avanzada(self):
        pass

    def consulta_basica(self):
        pass


# Corresponde a los usuarios jefes o
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
