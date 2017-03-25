# Usuarios v1.0.0

from abc import ABCMeta, abstractmethod
from leer import Users, Meteorology, Fire, Resources
from menu import Diccionario
from dibujar import frame


class Usuario(metaclass=ABCMeta):
    def __init__(self, dic):
        self.id = dic["id"]
        self.nombre = dic["nombre"]
        self.password = dic["contraseña"]
        self.recurso_id = dic["recurso_id"]

    def cerrar_sesion(self):
        opciones = {"": True}
        print("Si desea cerrar sesion click ENTER")
        print("cualquier otra tecla para anular...")
        eleccion = input("Respuesta: ")
        if eleccion in opciones:
            print("Sesion cerrada".center(60, "="))
            return True
        else:
            return False


# Corresponde al ususario ANAF
class Anaf(Usuario):
    def __init__(self, dic):
        super().__init__(dic)

    def crear_usuario(self):
        lexicon = Users().diccionario
        id = 0
        name = input("Ingrese el nombre del nuevo usuario: ")
        password = input("Ingrese la contraseña del nuevo usuario: ")
        salir = False
        while not salir:
            recurso = input("Ingrese el id de recurso si es necesario: ")
            if (recurso is "") or (recurso.isdigit()):
                salir = True
        while (True):
            if not (str(id) in Users().leer.keys()):
                id = str(id)
                break
            else:
                id += 1
        (lexicon["id"], lexicon["nombre"], lexicon["contraseña"], lexicon["recurso_id"]) = (id, name, password, recurso)
        Users().escribir(lexicon)

    def agregar_pronostico(self):
        necesarios = ["id", "fecha_inicio", "fecha_termino", "tipo", "valor", "lat", "lon", "radio"]
        opciones = {}
        for valores in necesarios:
            opciones[str(necesarios.index(valores))] = valores
        lexicon = Diccionario("pronostico", opciones).mostrar()
        print(lexicon)
        if lexicon != {}:
            Meteorology().escribir(lexicon)

    def agregar_incendio(self, lexicon):
        necesarios = Fire().diccionario.keys()
        opciones = {}
        for valores in necesarios:
            opciones[str(necesarios.index(valores))] = valores
        lexicon = Diccionario("pronostico", opciones).mostrar()
        print(lexicon)
        if lexicon != {}:
            Fire().escribir(lexicon)
        pass

    def leer_base(self):
        opciones = {"1": Users().leer, "2": Fire().leer, "3": Resources().leer}
        salir = False
        while not salir:
            print("1. leer usuarios")
            print("2. leer incendios")
            print("3. leer recursos")
            print("Otro. Salir")
            opcion = input("Respuesta: ")
            if opcion in opciones:
                terminar = False
                while not terminar:
                    print("1. leer todo")
                    print("2. leer linea")
                    print("3. leer por id")
                    print("Otro. Salir")
                    eleccion = input("Respuesta: ")
                    frame()
                    if eleccion is "1":
                        for i in range(len(opciones[opcion]) - 1):
                            for key, value in opciones[opcion][str(i + 1)].items():
                                print("{}: {}|".format(key, value), end="")
                            print("\n", end="")
                        print("".center(60, "="))
                    elif eleccion is "2":
                        finalizar = False
                        n = 1
                        while not finalizar:
                            print(opciones[opcion][str(n)])
                            print("1. Siguiente...")
                            print("2. Anterior...")
                            print("x. Terminar de leer")
                            respuesta = input("Respuesta: ")
                            if respuesta is "1":
                                if n < len(opciones[opcion]) - 1:
                                    n += 1
                                else:
                                    finalizar = True
                            elif respuesta is "2":
                                if n > 1:
                                    n -= 1
                                else:
                                    finalizar = True
                            elif respuesta is "x":
                                finalizar = True
                            frame()
                    elif eleccion is "3":
                        id = input("Ingrese id: ")
                        if id.isdigit() and id in opciones[opcion]:
                            for key, value in opciones[opcion][str(id)].items():
                                print("{}: {}".format(key, value), end="\n")
                            if "potencia" in opciones[opcion][str(id)]:
                                pass
                            elif "" in opciones[opcion][str(id)]:
                                pass
                    else:
                        terminar = True
            else:
                salir = True
            frame()


# Corresponde a los usuarios jefes o bomberos
class Terreno(Usuario):
    def __init__(self, dic):
        super().__init__(dic)
        pass
