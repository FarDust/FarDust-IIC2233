# brigadas v1.0.0
from abc import  ABCMeta

class Brigadas(metaclass=ABCMeta):
    def __init__(self, autonomia, descanso):
        self.autonomia = autonomia
        self.descanso = descanso

class AnafB(Brigadas):
    def __init__(self,autonomia , descanso):
        super().__init__(autonomia , descanso)

class Bomberos(Brigadas):
    def __init__(self, autonomia , descanso):
        super().__init__(autonomia , descanso)


