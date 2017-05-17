from abc import ABCMeta, abstractmethod
from collections import deque
from random import randint, random, choice


class Persona:
    def __init__(self, nombre: str, tipo="persona") -> None:
        """
        
        :param nombre: str
        :param tipo: str
        """
        self.name = nombre
        self.type = tipo

    def __repr__(self):
        return self.type + ": " + self.name


class Parlelismo(type):
    def __new__(mcs, name, bases, dic):
        return super().__new__(mcs, name, bases, dic)

    def __init__(cls, name, bases, dic):
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        alumno = super().__call__(*args, **kwargs)
        return alumno


class Alumno(Persona, metaclass=Parlelismo):
    """
    Esta clase representa a cada Alumno los cuales pueden generar avanze en una Evaluacion.
    """

    def __init__(self, nombre: str, seccion: int) -> None:
        """
        
        :param nombre: Nombre del alumno
        :type nombre: str
        :param seccion: Seccion del alumno
        :type seccion: int
        """
        super().__init__(nombre, tipo="Alumno")
        self.seccion = seccion
        self.personalidad = choice(["Eficiente", "Artistico", "Teorico"])
        self.confianza = randint(2, 12)
        self.contents = dict()
        self._contents_lvl = dict()
        self._set_credits()
        self.poketrainer_lvl = randint(1, 100)
        self.programing_lvl = randint(2, 10)
        self.acupaciones = deque()
        self.week = {"profesor": False, "fierta": False}
        self.atenticion = random()

    @property
    def horas(self):
        if self.creditos == 40:
            return 10, 25
        elif self.creditos == 55:
            return 10, 15
        elif self.creditos == 55:
            return 5, 15
        else:
            return 5, 10

    def _set_credits(self, p60=0.05, p40=0.1, p55=0.15, p50=0.7):
        n = random()
        if n < p60:
            self.creditos = 60
        elif n < p60 + p40:
            self.creditos = 40
        elif n < p60 + p40 + p55:
            self.creditos = 55
        elif n < p60 + p40 + p55 + p50:
            self.creditos = 50

    def aprender(self, content_name: str, dificultad: int):
        if content_name not in self.contents.keys():
            self.contents[content_name] = self._content_management(content_name, dificultad)
            self._contents_lvl[content_name] = 0

    def _content_management(self, content_name: str, dificultad: int):
        def content(horas: float):
            self._contents_lvl[content_name] += (1 / dificultad) * horas
            return self._contents_lvl[content_name]

        return content

    def bonus(self, materia: str, bonus: float):
        self._contents_lvl[materia] = self._contents_lvl[materia] * bonus

    def lvl_up(self):
        self.programing_lvl = 1.05 * (
            1 + (0.08 if self.week["profesor"] else 0) - (0.15 if self.week["fiesta"] else 0)) * self.programing_lvl
        # Reinicia el buff2er interno de eventos de la semana
        for i in self.week.keys():
            self.week[i] = False


class Profesor(Persona):
    def __init__(self, nombre: str, seccion: int):
        super().__init__(nombre, tipo="Profesor")
        self.seccion = seccion

    def resolver_duda(self, alumno):
        alumno.week["profesor"] = True

    @staticmethod
    def entregar_bonus(alumno, materia, cantidad: float):
        alumno.bonus(materia, cantidad)


class Ayudante(Persona):
    def __init__(self, nombre):
        super().__init__(nombre, tipo="Ayudante")


class Tareo(Ayudante):
    def __init__(self, nombre):
        super().__init__(nombre)


class Docencio(Ayudante):
    def __init__(self, nombre):
        super().__init__(nombre)
        self.dominados = []

    @staticmethod
    def disponibilidad():
        i = 0
        while i < 200:
            yield i
            i += 1

    @staticmethod
    def entregar_bonus(alumno, materia, cantidad: float):
        alumno.bonus(materia, cantidad)


class Coordinardor(Persona):
    def __init__(self, nombre):
        super().__init__(nombre, tipo="Coordinador")


if __name__ == "__main__":
    gabriel = Alumno("gabriel", 2)
    gabriel.aprender("funcional", 2)
