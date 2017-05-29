from random import choice
from time import sleep

from PyQt5.QtCore import QThread, QTimer, pyqtSignal

from objects.template import Objects
from scripts.attack import AttackEvent


class Tower(QThread, Objects):
    trigger = pyqtSignal(AttackEvent)
    attacking = pyqtSignal(QThread, int)

    def __init__(self, x, y, max_hp, atk_range, name, parent):
        super().__init__(pos=(x, y), maxhealth=max_hp)
        self.atk_range = atk_range
        self.basic_atk = 21
        self.name = name
        self.attacking.connect(parent.attack_trigger)
        self.posible_objetives = list()
        self.id = None
        self.start()

    def setid(self, value):
        self.id = value

    def less_hp(self, amount: AttackEvent):
        if self.currenthealth > 0:
            self.currenthealth -= amount.damage
            print(self.name, self.currenthealth)
        raise SystemExit

    def attack(self, objetive):
        print("{} emiting {}".format(self.name, objetive))
        self.attacking.emit(self, objetive)
        if len(self.posible_objetives) > 0:
            self.trigger.emit(AttackEvent(self.basic_atk))
            # self.trigger.disconnect()

    def run(self):
        while True:
            if len(self.posible_objetives) > 0:
                self.attack(choice(self.posible_objetives))
            sleep(1)
