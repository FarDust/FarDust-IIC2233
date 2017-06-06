from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from objects.units.units import Unit
from scripts.animation import Animation


class Minion(Unit):
    def __init__(self, mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp)
        self.objective = None


class Normal(Minion):
    def __init__(self, x, y, front, mov_speed=8, basic_atk=2, atk_speed=1, atk_range=5, max_hp=45):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, (x, y), max_hp)
        self.image = Animation("IMGS/units/minions/small/front/", front)


class Grande(Minion):
    def __init__(self, x, y, front, mov_speed=8, basic_atk=4, atk_speed=1, atk_range=20, max_hp=60):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, (x, y), max_hp)
        self.image = Animation("IMGS/units/minions/big/front/", front)
