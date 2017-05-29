from PyQt5.QtCore import QThread, QTimer, pyqtSignal

from objects.template import Objects
from scripts.attack import AttackEvent


class Tower(QThread, Objects):
    trigger = pyqtSignal(AttackEvent)
    def __init__(self, x, y, max_hp, atk_range,name):
        super().__init__(pos=(x, y), maxhealth=max_hp)
        self.atk_range = atk_range
        self.basic_atk = 21
        self.name= name
        self.triggers = list()
        self.start()

    def less_hp(self, amount: AttackEvent):
        if self.currenthealth > 0:
            self.currenthealth -= amount.damage
            print(self.name,self.currenthealth)

    def _attack(self):
        if len(self.triggers) > 0:
            self.trigger.emit(AttackEvent(self.basic_atk))

    def run(self):
        while True:
            self._attack()
        pass
