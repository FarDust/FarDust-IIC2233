from PyQt5.QtCore import QTimer


class Objects():
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
        self.id = None

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
