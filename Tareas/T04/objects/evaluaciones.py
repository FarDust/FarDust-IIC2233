class Evaluacion(type):
    def __new__(mcs, name, bases, dic):
        return super().__new__(mcs, name, bases, dic)

    def __init__(cls, name, bases, dic):
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


def identificador():
    i = 1
    while True:
        yield i
        i += 1


class Actividad(metaclass=Evaluacion):
    _actividades = []

    def __init__(self, numero):
        self.name = "Actividad {}".format(numero)
        self.numero = numero
        self._actividades.append(numero)
        self.combat_lvl = 0

    def set_combat_lvl(self, lvl):
        self.combat_lvl = lvl

    def __getitem__(self, item):
        return self._actividades[item]

    def __copy__(self):
        return type(self.name, (Actividad,), {"progress": 0})

    def __str__(self):
        return self.name


class Tarea(metaclass=Evaluacion):
    pass


class Control(metaclass=Evaluacion):
    pass


class Examen(metaclass=Evaluacion):
    pass


if __name__ == "__main__":
    pass
