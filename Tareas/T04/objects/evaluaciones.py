from random import random, randint


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

    def __init__(self, numero: int, materia: str, dificultad: int):
        self.name = "Actividad {}".format(numero)
        self.materia = materia
        self.numero = numero
        self._actividades.append(numero)
        self.combat_lvl = 0
        self.dificultad = dificultad
    @property
    def exigencia(self):
        return 7 + randint(1, 5) / self.dificultad

    def set_combat_lvl(self, lvl):
        self.combat_lvl = lvl

    def __getitem__(self, item):
        return self._actividades[item]

    def getcopy(self):
        @property
        def total_progress(new):
            return 0.4 * new.progress_func + 0.4 * new.progress_cont + 0.2 * new.progress_pep

        @property
        def nota_final(new):
            return max((new.total_progress / new.exigencia) * 7, 1)

        def __repr__(new):
            return "{} - progress: {}".format(new.name, new.total_progress)

        return type(self.name, (Actividad,),
                    {"progress_func": 0, "progress_cont": 0, "progress_pep": 0, "total_progress": total_progress,
                     "__repr__": __repr__, "nota_final": nota_final})(
            self.numero, self.materia, self.dificultad)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return self.name


class Tarea(metaclass=Evaluacion):
    pass


class Control(metaclass=Evaluacion):
    pass


class Examen(metaclass=Evaluacion):
    pass


if __name__ == "__main__":
    a1 = Actividad(2, "gatos")
    a2 = a1.getcopy()
    print(a2.total_progress)
    a2.progress_cont = 2
    print(a2.total_progress)
