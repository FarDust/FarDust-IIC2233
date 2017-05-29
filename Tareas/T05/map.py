from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QObject
from scripts.utils import distancia
from scripts.attack import AttackEvent


class Map(QThread):
    def __init__(self, width: int, height: int):
        super().__init__()
        self.objects = list()
        self.triggered = dict()
        for i in self.objects:
            self.triggered[i] = dict()

    @staticmethod
    def on_range(unit1, unit2):
        if unit1 != unit2 and distancia(*unit1.pos, *unit2.pos) <= unit1.atk_range:
            return True
        else:
            return False

    def get_object(self, target):
        self.objects.append(target)
        self.triggered[target] = dict()

    def attack_trigger(self):
        for unit1 in self.objects:
            for unit2 in self.objects:
                if self.on_range(unit1, unit2):
                    unit1.triggers.append(pyqtSignal(AttackEvent))
                    self.triggered[unit1][unit2] = unit1.triggers[-1]
                    #unit1.triggers[-1].connect(unit2.less_hp)
                    unit1.trigger.connect(unit2.less_hp)
                elif unit2 in self.triggered[unit1].keys():
                    signal = self.triggered[unit1][unit2]
                    index = unit1.triggers.index(signal)
                    unit1.triggers[index].disconnect()
                    unit1.triggers.remove(signal)

    def run(self):
        while True:
            self.attack_trigger()


if __name__ == '__main__':
    pass
