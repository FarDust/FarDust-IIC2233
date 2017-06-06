from random import randint

from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QObject, pyqtSlot

from objects.buildings.nexo import Nexo
from objects.units.subditos import Minion, Normal, Grande
from scripts.movement import MoveMyImageEvent
from scripts.utils import distancia


def identifier():
    i = 0
    while True:
        yield i
        i += 1


class Map(QThread):
    ids = identifier()
    show_minion = pyqtSignal(MoveMyImageEvent)

    def __init__(self, front, width: int = 1600, height: int = 900):
        super().__init__()
        self.objects = list()
        self.front = front
        self.show_minion.connect(front.actualizar)

    @staticmethod
    def on_range(unit1, unit2):
        x1 = unit1.pos[0] + unit1.image.width() // 2
        y1 = unit1.pos[1] + 5 * unit1.image.height() // 6
        x2 = unit1.pos[0] + unit2.image.width() // 2
        y2 = unit2.pos[1] + 5 * unit2.image.height() // 6
        if unit1 != unit2 and distancia(x1, y1, x2, y2) <= unit1.atk_range:
            return True
        else:
            return False

    @staticmethod
    def move_player(movement_signal):
        pass

    def get_player(self, target, front):
        front.movement.connect(target.get_rules)
        self.get_object(target)

    def get_object(self, target):
        if isinstance(target, Nexo):
            target.spawn.connect(self.spawn_minion)
        target.setid(next(self.ids))
        self.objects.append(target)

    # @pyqtSlot(name="attack")
    def attack_trigger(self, unit1, attack):
        if attack in unit1.posible_objetives:
            unit2 = next(filter(lambda x: x.id == attack, self.objects))
            if self.on_range(unit1, unit2) and not unit1.death:
                print("get {} from {}".format(attack, unit1.name))
                print(unit1.name, "attacking ->", unit2.name)
                unit1.trigger.connect(unit2.less_hp)
        else:
            print("Fail")

    def attack_selector(self):
        for unit1 in self.objects:
            for unit2 in self.objects:
                if unit1 != unit2 and unit2.id not in unit1.posible_objetives and self.on_range(unit1, unit2) \
                        and not unit2.death and not unit1.death:
                    print(unit1.name, "add", unit2.name, "as objetive")
                    unit1.posible_objetives.append(unit2.id)
                elif (not self.on_range(unit1,
                                        unit2) or unit2.death or unit1.death) and unit2.id in unit1.posible_objetives:
                    print(unit1.name, "remove", unit2.name, "as objetive")
                    unit1.posible_objetives.remove(unit2.id)

    def spawn_minion(self):
        nexus = self.sender()
        # noinspection PyTypeChecker
        new_minions = [Normal(nexus.pos[0] + 5, nexus.pos[1] + 5, self.front) for _ in range(4)] + [
            Grande(nexus.pos[0], nexus.pos[1], self.front)]
        for minion in new_minions:
            self.show_minion.emit(MoveMyImageEvent(minion.image, *minion.pos))
            self.get_object(minion)

    def run(self):
        while True:
            self.attack_selector()


if __name__ == '__main__':
    pass
