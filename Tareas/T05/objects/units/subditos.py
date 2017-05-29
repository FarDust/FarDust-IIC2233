from objects.units.units import Unit


class Minion(Unit):
    def __init__(self, mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp)
        self.objective = None

    def getobjetive(self, objective):
        self.objective = objective

    def attack(self):
        self.objective.currenthealth -= self.atk
