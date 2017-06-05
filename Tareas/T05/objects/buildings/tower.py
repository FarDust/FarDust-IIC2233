from random import choice
from time import sleep

from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel

from objects.template import Objects
from scripts.attack import AttackEvent


class Tower(QThread, Objects):
    trigger = pyqtSignal(AttackEvent)
    attacking = pyqtSignal(QThread, int)

    def __init__(self,front , x, y, max_hp, atk_range, name, backend, atk_dmg):
        super().__init__(pos=(x, y), maxhealth=max_hp)
        image = QPixmap("resources/buildings/tower/0.png")
        image = image.scaled(image.width()*0.8, image.height()*0.8)
        self.image = QLabel("", front)
        self.image.setGeometry(x, y, image.width(), image.height())
        self.image.setPixmap(image)
        self.atk_range = atk_range
        self.basic_atk = atk_dmg
        self.atk_speed = 2.55
        self.name = name
        self.attacking.connect(backend.attack_trigger)
        self.posible_objetives = list()
        self.start()

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
