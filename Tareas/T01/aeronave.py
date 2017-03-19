# Aeronave v1.0.0

from abc import ABCMeta


class Aeronave(metaclass=ABCMeta):
    def __init__(self, autonomia, descanso):
        self.autonomia = autonomia
        self.descanso = descanso


class Avion(Aeronave):
    def __init__(self, autonomia, descanso):
        super().__init__(autonomia, descanso)


class Helicoptero(Aeronave):
    def __init__(self, autonomia, descanso):
        super().__init__(autonomia, descanso)
