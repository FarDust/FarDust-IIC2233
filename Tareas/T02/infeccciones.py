from super_lista import Lista
from abc import ABCMeta, abstractmethod


class Infecciones(metaclass=ABCMeta):
    def __init__(self, contagiosisdad=0.0, mortalidad=0.0, resistencia=0.0, visibilidad=0.0, **kwargs):
        self.contagiosidad = contagiosisdad
        self.mortalidad = mortalidad
        self.resistencia = resistencia
        self.visibilidad = visibilidad


class Virus(Infecciones):
    super().__init__(contagiosisdad=1.5, mortalidad=1.2, resistencia=1.5, visibilidad=0.5)


class Bacteria(Infecciones):
    super().__init__(contagiosisdad=1.0, mortalidad=1.0, resistencia=0.5, visibilidad=0.7)


class Parasito(Infecciones):
    super().__init__(contagiosisdad=0.5, mortalidad=1.5, resistencia=1.0, visibilidad=0.45)


