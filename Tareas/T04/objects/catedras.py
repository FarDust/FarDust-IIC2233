from random import choice
from objects.people import Profesor, Alumno, Docencio


def crear_secciones(base_datos: str) -> dict:
    header = list(
        head[:head.find(":")] for head in list(next(open(base_datos, "r", encoding="utf8")).strip().split(",")))
    secciones = dict()
    for info in filter(lambda linea: linea.find("Profesor") != -1, open(base_datos, "r", encoding="utf8")):
        info = info.strip().split(",")
        profesor = Profesor(info[header.index("Nombre")], int(info[header.index("Sección")]))
        alumnos = list()
        for person in filter(lambda linea: linea.find("Alumno") != -1 and linea.find(info[header.index("Sección")]),
                             open(base_datos, "r", encoding="utf8")):
            person = person.strip().split(",")
            alumnos.append(Alumno(person[header.index("Nombre")], int(person[header.index("Sección")])))
        secciones[info[header.index("Sección")]] = Seccion(int(info[header.index("Sección")]), alumnos, profesor)
    return secciones


class Seccion:
    def __init__(self, numero, alumnos, profesor):
        self.numero = numero
        self.alumnos = alumnos
        self.profesor = profesor

    def __repr__(self):
        return str(self.profesor) + "\n" + "\n".join(list(str(i) for i in self.alumnos))


class Ayudantia:
    def __init__(self, alummnos, ayudantes):
        pass


def catedra(seccion: Seccion, materia: str):
    def catedrita() -> None:
        from random import random
        for alumno in seccion.alumnos:
            if random() > alumno.atenticion:
                seccion.profesor.entregar_bonus(alumno, materia, .1)
    return catedrita






if __name__ == "__main__":
    seccion = crear_secciones("../integrantes.csv")
    print(seccion["2"])
