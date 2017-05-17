from objects.evaluaciones import Actividad
from objects.catedras import *


class Evento:
    def __init__(self, tipo, acciones, tiempo):
        """
        
        :param tiempo: dia de ocurrencia de evento 
        :type tiempo: int
        :param tipo: tipo del evento creado
        :type tipo: class
        :param accion: 
        :type accion: function
        """
        self.tipo = tipo
        self.tiempo = tiempo
        self.acciones = acciones

    def start(self):
        """
        Ejecuta todas las acciones en el evento y devuelve todos los resultados
        :return: resultados de las consultas
        :type: tuple
        """
        return tuple(*[func() for func in self.acciones])

    def __str__(self):
        return str(self.tipo)

    def __repr__(self):
        return str(self.tipo) + " -> {}".format(self.tiempo)


class ColaEventos(list):
    pass


tipos = {}


def simular(materias):
    dia = 1
    semana = 1
    eventos = []
    establecer_actividades(eventos, 12)
    eventos = crear_catedra(eventos, crear_secciones("integrantes.csv"), 4, materias)
    while semana <= len(materias):
        if len(eventos) != 0:
            eventos = sorted(eventos, key=lambda x: x.tiempo)
        for evento in filter(lambda x: x.tiempo == dia, eventos):
            evento.start()
            eventos.remove(evento)
            print(evento, dia)
        dia += 1
        if dia % 7 == 0:
            semana += 1


def establecer_actividades(events: list, n: int) -> list:
    for i in range(n):
        events.append((Evento(Actividad(i + 1), tuple(), (i + 4) + i * 6)))
    return sorted(events, key=lambda x: x.tiempo)


def crear_catedra(events: list, secciones: dict, dia: int, materias, contents=None) -> list:
    if contents is None:
        contents = iter(materias)
    if len(materias) > 0:
        for seccion in secciones.values():
            events.append(
                Evento("Catedra", (
                    catedra(seccion, next(contents)),
                    crear_catedra(events, secciones, dia + 7, materias[1:], contents)),
                       dia))
        return events
    return events


profesores = dict()
alumnos = dict()
docencios = dict()
tareos = dict()

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
    simular(list(materias.keys()))
