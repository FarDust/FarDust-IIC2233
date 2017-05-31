from random import choice
from time import sleep

from PyQt5.QtCore import pyqtSignal, QThread

from objects.template import Objects
from scripts.attack import AttackEvent


class Unit(QThread,Objects):
    trigger = pyqtSignal(AttackEvent)
    attacking = pyqtSignal(QThread, int)

    def __init__(self, mov_speed: int, basic_atk: int, atk_speed: float, atk_range: float, pos: tuple, max_hp: int = 0):
        super().__init__(pos=pos, maxhealth=max_hp)
        self.mov_speed = mov_speed
        self.atk = basic_atk
        self.atk_speed = atk_speed
        self.atk_range = atk_range
        self.posible_objetives = list()
        self.name = ""

    def less_hp(self, amount: AttackEvent):
        if self.currenthealth > 0 and not self.death:
            self.currenthealth -= min(amount.damage, self.currenthealth)
            print(self.name, "loss {} of life".format(amount.damage))
            print(self.name,":",self.currenthealth)

    def attack(self, objetive):
        if not self.death:
            print("{} emiting {}".format(self.name, objetive))
            self.attacking.emit(self, objetive)
            if len(self.posible_objetives) > 0 and not self.death:
                self.trigger.emit(AttackEvent(self.basic_atk))

    def run(self):
        while True:
            if len(self.posible_objetives) > 0:
                self.attack(choice(self.posible_objetives))
            sleep(1/self.atk_speed)
