from PyQt5.QtCore import QTimer, pyqtSignal

from scripts.movement import MoveMyImageEvent


class Objects():
    mimage = pyqtSignal(MoveMyImageEvent)
    def __init__(self, pos: tuple, maxhealth: int = 0):
        self.pos = pos
        self.maxhealth = maxhealth
        self.inmune = False
        if self.maxhealth == 0:
            self.inmune = True
        self.currenthealth = maxhealth
        self.posible_objetives = list()
        self.atk_range = 0
        self._regeneration = QTimer(self)
        self._regeneration.timeout.connect(self.regeneration)
        self._regeneration.start(1000)
        self.__position = pos
        self.id = None

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.pos = (value[0], value[1])
        self.mimage.emit(
            MoveMyImageEvent(self.image, self.position[0], self.position[1]))

    def setid(self, value):
        self.id = value

    def regeneration(self):
        if self.maxhealth > 0 and not self.death and self.currenthealth < self.maxhealth:
            self.currenthealth += min(self.maxhealth*0.01, self.maxhealth-self.currenthealth)
            print(self.currenthealth)

    @property
    def death(self):
        if not self.inmune and self.currenthealth < 1:
            return True
        else:
            return False
