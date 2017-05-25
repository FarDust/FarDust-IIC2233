from objects.units.units import Unit

all_habilities = dict()


class Champion(Unit):
    def __init__(self, mov_speed: int = 0, basic_atk: int = 0, atk_speed: float = 0.0, atk_range: float = 0.0,
                 pos: tuple = (0, 0), max_hp: int = 0, habilidades: str = "", **kwargs):
        super().__init__(mov_speed, basic_atk, atk_speed, atk_range, pos, max_hp)
        self.habilidades = list()
        for habilidad in habilidades.split(","):
            self.habilidades.append(all_habilities[habilidad])
        pass


if __name__ == '__main__':
    from scripts.readers import read_properties

    test = {"gato": "100"}
    champ = Champion(**test)
    # Champion(**read_properties(path))
