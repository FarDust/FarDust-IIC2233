from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from objects.units.units import Unit
from scripts.movement import MoveMyImageEvent, movement_listener
from resources.animation import player
from scripts.utils import distancia

all_habilities = dict()


class Champion(Unit):
    def __init__(self, mov_speed: int = 0, basic_atk: int = 0, atk_speed: float = 0.0, atk_range: float = 0.0,
                 pos: tuple = (0, 0), max_hp: int = 0, habilidades: str = "", name: str = "", **kwargs):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp)
        self.habilidades = list()
        if habilidades != "":
            for habilidad in habilidades.split(","):
                self.habilidades.append(all_habilities[habilidad])
        self.death_count = 0
        self.trb = 10
        self.name = name
        pass

    @property
    def death_delay(self):
        return self.trb * 1.1 ** self.death_count


class Character(Champion):
    trigger = pyqtSignal(MoveMyImageEvent)

    def __init__(self, front, x, y, imagen, champion):
        print(champion)
        super().__init__(pos=(x, y), **champion)
        self.mov_speed = 2
        self.image = QLabel(front)
        self.animation = player
        image = QPixmap(imagen)
        image.scaled(25, 25)
        self.rules = None
        self.image.setGeometry(0, 0, image.width(), image.height())
        self.image.setPixmap(image)
        self.image.show()
        self.image.setVisible(True)
        self.trigger.connect(front.actualizar_jugador)
        self.__position = (0, 0)
        self.position = (x, y)
        self.movement = QThread()
        self.movement.__setattr__("run", self.move)
        self.start()

    def run(self):
        super().start()
        while True:
            pass

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        if not self.rules:
            rules = list()
        else:
            rules = self.rules.keys
        self.trigger.emit(
            MoveMyImageEvent(self.image, self.position[0], self.position[1], rules, self.animation))

    def get_rules(self, rules):
        self.rules = rules
        self.movement.start()

    def move(self):
        rules = self.rules
        (x2, y2) = rules.cursor
        x1 = self.position[0]
        y1 = self.position[1]
        hip = distancia(x1, y1, x2, y2)

        if 38 in rules.keys or 87 in rules.keys:
            x = ((x2 - x1) / hip) * self.mov_speed * 1
            y = ((y2 - y1) / hip) * self.mov_speed * 1
            self.position = (x1 + x, y1 + y)
        elif 40 in rules.keys or 83 in rules.keys:
            x = ((x2 - x1) / hip) * self.mov_speed * -1
            y = ((y2 - y1) / hip) * self.mov_speed * -1
            self.position = (x1 + x, y1 + y)

        if 37 in rules.keys or 65 in rules.keys:
            x = ((y2 - y1) / hip) * self.mov_speed * 1
            y = ((x2 - x1) / hip) * self.mov_speed * 1
            self.position = (x1 + x, y1 - y)
        elif 39 in rules.keys or 68 in rules.keys:
            x = ((y2 - y1) / hip) * self.mov_speed * -1
            y = ((x2 - x1) / hip) * self.mov_speed * -1
            self.position = (x1 + x, y1 - y)


if __name__ == '__main__':
    test = {"gato": "100"}
    champ = Champion(**test)
