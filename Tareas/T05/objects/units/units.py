from objects.template import Objects


class Unit(Objects):
    def __init__(self, mov_speed: int, basic_atk: int, atk_speed: float, atk_range: float, pos: tuple, max_hp: int = 0):
        super().__init__(pos=pos, maxhealth=max_hp)
        self.mov_speed = mov_speed
        self.atk = basic_atk
        self.atk_speed = atk_speed
        self.atk_range = atk_range

