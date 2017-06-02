from PyQt5.QtCore import pyqtSignal, QThread
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
        self.image.setGeometry(0, 0, image.width(), image.height())
        self.image.setPixmap(image)
        self.image.show()
        self.image.setVisible(True)
        self.quarry = list()
        self.trigger.connect(front.actualizar_jugador)
        self.__position = (0, 0)
        self.position = (x, y)
        self.start()

    def run(self):
        super().run()
        while True:
            if len(self.quarry) > 0:
                movement_listener(self, self.quarry)
                self.quarry.clear()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        self.trigger.emit(MoveMyImageEvent(self.image, self.position[0], self.position[1], self.quarry, self.animation))

    def getImportartKeys(self, keylist):
        filtro = {37, 38, 39, 40}
        self.quarry = list(filter(lambda x: x in filtro, keylist))

    def move(self, rules):
        print(rules.keys)
        (factor, cofactor, reset) = (0, 0, 1)
        if 38 in rules.keys or 87 in rules.keys:
            factor = 1
        elif 40 in rules.keys or 83 in rules.keys:
            factor = -1
        if 37 in rules.keys or 65 in rules.keys:
            cofactor = 1
            reset = -1
        elif 39 in rules.keys or 68 in rules.keys:
            cofactor = -1
            reset = -1
        (x2, y2) = rules.cursor
        x1 = self.position[0]
        y1 = self.position[1]
        hip = distancia(x1, y1, x2, y2)
        x = ((x2 - x1) / hip) * self.mov_speed * factor + ((y2 - y1) / hip) * self.mov_speed * cofactor
        y = ((y2 - y1) / hip) * self.mov_speed * factor + ((x2 - x1) / hip) * self.mov_speed * cofactor
        self.position = (x1 + x, y1 + y*reset)


if __name__ == '__main__':
    from scripts.readers import read_properties

    test = {"gato": "100"}
    champ = Champion(**test)
    # Champion(**read_properties(path))
