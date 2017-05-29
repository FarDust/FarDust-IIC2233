from PyQt5.QtCore import QTimer


class AttackEvent():
    def __init__(self, damage):
        self.damage = damage
        pass

class Attack(QTimer):
    def __init__(self,unit):
        super().__init__()



