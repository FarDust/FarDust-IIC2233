from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QObject, pyqtSlot

from scripts.utils import distancia


def identifier():
    i = 0
    while True:
        yield i
        i += 1


class Map(QThread):
    ids = identifier()

    def __init__(self, width: int, height: int):
        super().__init__()
        self.objects = list()

    @staticmethod
    def on_range(unit1, unit2):
        if unit1 != unit2 and distancia(*unit1.pos, *unit2.pos) <= unit1.atk_range:
            return True
        else:
            return False

    def get_object(self, target):
        target.setid(next(self.ids))
        self.objects.append(target)

    # @pyqtSlot(name="attack")
    def attack_trigger(self, unit1, attack):
        print("resive {} from {}".format(attack, unit1.name))
        if attack in unit1.posible_objetives:
            unit2 = next(filter(lambda x: x.id == attack, self.objects))
            print(unit1.name, "attacking ->", unit2.name)
            if self.on_range(unit1, unit2):
                unit1.trigger.connect(unit2.less_hp)
        else:
            print("Fail")

    def attack_selector(self):
        for unit1 in self.objects:
            for unit2 in self.objects:
                if unit1 != unit2 and unit2.id not in unit1.posible_objetives and self.on_range(unit1, unit2):
                    print(unit1.name, "added", unit2.name, "as objetive")
                    unit1.posible_objetives.append(unit2.id)
                elif not self.on_range(unit1, unit2) and unit2.id in unit1.posible_objetives:
                    unit1.posible_objetives.remove(unit2.id)

    def run(self):
        while True:
            self.attack_selector()


if __name__ == '__main__':
    pass
