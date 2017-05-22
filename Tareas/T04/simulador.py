from objects.evaluaciones import Actividad
from objects.catedras import *


class Evento:
    def __init__(self, tipo, acciones, tiempo, prioridad):
        """
        
        :param tiempo: dia de ocurrencia de evento 
        :type tiempo: int
        :param tipo: tipo del evento creado
        :type tipo: class
        :param acciones: 
        :type acciones: tuple
        """
        self.tipo = tipo
        self.tiempo = tiempo
        self.acciones = acciones
        self.prioridad = prioridad
        self._results = list()

    @property
    def results(self):
        return list(filter(lambda x: x is not None, self._results))

    def start(self):
        """
        Ejecuta todas las acciones en el evento
        """
        if __name__ == "__main__" and self.get_type != Alumno:
            print("{} working...".format(self))
        self._results = [func() for func in self.acciones]

    @property
    def get_type(self):
        if type(self.tipo) == str:
            return self.tipo
        else:
            return type(self.tipo)

    def __str__(self):
        return str(self.tipo) + " -> day: {}".format(self.tiempo)

    def __repr__(self):
        return str(self.tipo) + " -> day: {}".format(self.tiempo)


def simular(materias: dict):
    for dificultad in materias.values():
        if dificultad <= 0:
            print("Mala persona!!! -> todo tiene dificultad en la vida")
            raise SystemExit
    (dia, semana) = (1, 1)
    eventos = []
    secciones = crear_secciones("integrantes.csv")
    alumnos = list()
    for seccion in secciones.values():
        for alumno in seccion.alumnos:
            alumnos.append(alumno)
    iniciar_semanas(eventos, alumnos, list(materias.keys()))
    for seccion in secciones.values():
        for alumno in seccion.alumnos:
            [alumno.aprender(contenido, dificultad) for contenido, dificultad in materias.items()]
    agendar_actividades(eventos, materias)
    crear_catedra(eventos, secciones, 4, list(materias.keys()))
    while semana <= len(materias) or len(eventos) != 0:
        if len(eventos) != 0:
            eventos = sorted(eventos, key=lambda x: x.tiempo)
        for evento in sorted(list(filter(lambda x: x.tiempo == dia, eventos)), key=lambda x: x.prioridad):
            evento.start()
            if evento.get_type == Actividad:
                publicar_actividad(secciones, evento.tipo)
            eventos.remove(evento)
        dia += 1
        if dia % 7 == 0:
            semana += 1


def agendar_actividades(events: list, contenidos: dict) -> list:
    for i in range(len(contenidos)):
        actual = list(contenidos.keys())[i]
        events.append((Evento(Actividad(i + 1, actual, contenidos[actual]), tuple(), (i + 4) + i * 6, 3)))
    return sorted(events, key=lambda x: x.tiempo)


def crear_catedra(events: list, secciones: dict, dia: int, materias: list) -> None:
    contents = iter(materias)
    if len(materias) > 0:
        content = next(contents)
        for seccion in secciones.values():
            events.append(Evento("Catedra", (catedra(seccion, content),), dia, 2))
        crear_catedra(events, secciones, dia + 7, materias[1:])


def iniciar_semanas(events, alumnos, materias, dia=1):
    if len(materias) > 0:
        materia = materias.pop(0)
        iniciar_semanas(events, alumnos, materias, dia + 7)
        for alumno in alumnos:
            func = alumno.calcular_semana(materia)
            for i in range(7):
                events.append(Evento(alumno, (func, alumno.exec_dia), dia + i, 1))


def publicar_actividad(secciones, actividad):
    actividades = list()
    for seccion in secciones.values():
        for alumno in seccion.alumnos:
            actividades.append(alumno.resolver_actividad(actividad.getcopy()))
    return actividades



if __name__ == "__main__":
    materias = {"Programacion orientada a objeto": 2,
                "Herencia, composicion y agregacion": 2,
                "Listas, set y diccionario": 3,
                "Arbol y grafos": 5,
                "Funcional": 7,
                "Metaclases": 10,
                "Simulacion": 7,
                "Threading": 9,
                "Interfaz Grafica": 1,
                "Bytes y Serializacion": 6,
                "Networking": 6,
                "Webservices": 5
                }
    simular(materias)
