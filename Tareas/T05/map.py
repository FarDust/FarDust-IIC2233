from PyQt5.QtCore import QThread, QTimer, pyqtSignal
from scripts.utils import distancia
from scripts.attack import AttackEvent



class Map():
    def __init__(self, width: int, height: int):
        super().__init__()
        self.objects = list()
        self.triggered = dict()
        for i in self.objects:
            self.triggered[i] = dict()
        self.range_selector = QThread()
        self.range_selector.__setattr__("run", self.attack_trigger)
        self.range_selector.start()

    @staticmethod
    def on_range(unit1, unit2):
        print(distancia(*unit1, *unit2), unit1.atk_range)
        if distancia(*unit1, *unit2) <= unit1.atk_range:
            return True
        else:
            return False

    def get_object(self, target):
        self.objects.append(target)
        self.triggered[target] = dict()

    def attack_trigger(self):
        while True:
            for unit1 in self.objects:
                for unit2 in self.objects:
                    if self.on_range(unit1, unit2):
                        signal = pyqtSignal(AttackEvent)
                        self.triggered[unit1][unit2] = signal
                        unit1.triggers.append(signal)
                        unit1.triggers[-1].connect(unit2.less_hp)
                    elif unit2 in self.triggered[unit1].keys():
                        signal = self.triggered[unit1][unit2]
                        index = unit1.triggers.index(signal)
                        unit1.triggers[index].disconnect()
                        unit1.triggers.remove(signal)


if __name__ == '__main__':
    from objects.buildings.tower import Tower
    from time import time, sleep

    a = Tower(1, 2, 200, 10)
    b = Tower(1, 4, 200, 10)
    back = Map(600, 600)
    back.get_object(a)
    back.get_object(b)
    sleep(10)
    pass
