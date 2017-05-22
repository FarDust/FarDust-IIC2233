from abc import ABCMeta, abstractmethod
from collections import deque
from random import randint, random, choice
from modules.log import log

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
        self._set_horas_semana()
        self.poketrainer_lvl = randint(1, 100)
        self.programing_lvl = randint(2, 10)
        self.ocupaciones = deque()
        self.week = {"profesor": False, "fiesta": False}
        self.fiesta_countdown = 0
        self.atenticion = random()
        self.actividades = set()
        self.tarea_actual = None
        self.enfoque = None

    @property
    def horas(self) -> tuple:
        """
        
        :return: Rango de horas en la semana disponibles
        :type: tuple
        """
        if self.creditos == 40:
            return 10, 25
        elif self.creditos == 55:
            return 10, 15
        elif self.creditos == 55:
            return 5, 15
        else:
            return 5, 10

    def _set_credits(self, p60=0.05, p40=0.1, p55=0.15, p50=0.7):
        """
        
        :param p60: propabilidad 60 creditos
        :type: p60: float
        :param p40: propabilidad 40 creditos
        :type: p40: float
        :param p55: propabilidad 55 creditos
        :type: p55: float
        :param p50: propabilidad 50 creditos
        :type: p50: float
        """
        n = random()
        if n < p60:
            self.creditos = 60
        elif n < p60 + p40:
            self.creditos = 40
        elif n < p60 + p40 + p55:
            self.creditos = 55
        elif n < p60 + p40 + p55 + p50:
            self.creditos = 50

    def aprender(self, content_name: str, dificultad: int) -> None:
        """
        Funcion encargada de adquirir conocimientos
        
        :param content_name: nombre del contenido 
        :type content_name: str
        :param dificultad: dificultad del contenido
        :type: int
        """
        if content_name not in self.contents.keys():
            self.contents[content_name] = self._content_management(content_name, dificultad)
            self._contents_lvl[content_name] = 0

    def _content_management(self, content_name: str, dificultad: int):
        def content(horas: float = 0.0):
            self._contents_lvl[content_name] += (1 / dificultad) * horas
            return self._contents_lvl[content_name]

        return content

    def bonus(self, materia: str, bonus: float):
        self._contents_lvl[materia] = self._contents_lvl[materia] * bonus

    def _lvl_up(self):
        self.programing_lvl = 1.05 * (
            1 + (0.08 if self.week["profesor"] else 0) - (0.15 if self.week["fiesta"] else 0)) * self.programing_lvl
        # Reinicia el buffer interno de eventos de la semana
        for i in self.week.keys():
            self.week[i] = False
        log("programing lvl: {}".format(self.programing_lvl), "alumnos/{}".format(self.name))

    def _get_activity(self, actividad):
        self.actividades.add(actividad)

    def resolver_actividad(self, actividad):
        if not any(tuple(type(work) == type(actividad) for work in self.actividades)):
            self._get_activity(actividad)

        def progress(content, programming, confianza):
            return content * self.contents[
                actividad.materia]() + programming * self.programing_lvl + confianza * self.confianza

        actividad.progress_pep = progress(.7, .2, .1)
        actividad.progress_cont = progress(.7, .2, .1)
        actividad.progress_func = progress(.3, .6, .1)
        return actividad

    def resibir_tarea(self, tarea):
        self.tarea_actual = tarea
        pass

    def entregar_tarea(self):
        tarea = self.tarea_actual
        self.tarea_actual = None
        return tarea

    def _trabajar_tarea(self):
        if self.tarea_actual:
            self.horas_disponibles_semana -= (self.horas_disponibles_semana / 7) * .7
            self.contents[self.enfoque]((self.horas_disponibles_semana / 7) * .7)
        pass

    def _set_horas_semana(self):
        self.horas_disponibles_semana = randint(*self.horas)

    def _estudiar_materia(self):
        self.horas_disponibles_semana -= (self.horas_disponibles_semana / 7) * .3
        self.contents[self.enfoque]((self.horas_disponibles_semana / 7) * .3)

    def calcular_semana(self, materia):
        self._lvl_up()
        self._set_horas_semana()
        self.enfoque = materia
        return self.programar_dia

    def programar_dia(self):

        if self.fiesta_countdown == 0:
            self.ocupaciones.append(self._estudiar_materia)
            self.ocupaciones.append(self._trabajar_tarea)
        else:
            self.fiesta_countdown -= 1

    def exec_dia(self):
        [ocupacion() for ocupacion in self.ocupaciones]

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
        self.notas = dict()

    def recibir_notas(self, evaluaciones):
        self.notas[evaluaciones[0].name] = evaluaciones

if __name__ == "__main__":
    gabriel = Alumno("gabriel", 2)
    gabriel.aprender("funcional", 2)
    from objects.evaluaciones import Actividad

    gabriel.aprender("gatos", 100000)
    gabriel.resolver_actividad(Actividad(1, "gatos").getcopy())
    print(gabriel.actividades)
