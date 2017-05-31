from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from objects.units.units import Unit
from scripts.movement import MoveMyImageEvent, movement_listener
from resources.animation import player

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


if __name__ == '__main__':
    from scripts.readers import read_properties

    test = {"gato": "100"}
    champ = Champion(**test)
    # Champion(**read_properties(path))
