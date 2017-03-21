# Menu v1.0.1

from abc import ABCMeta, abstractmethod
from dibujar import frame


class Menu(metaclass=ABCMeta):
    def __init__(self, nombre, opciones=None):
        if opciones is None:
            opciones = {}
        self.opciones = opciones
        self.nombre = nombre

    @abstractmethod
    def mostrar(self):
        pass

    @abstractmethod
    def entrada(self):
        pass


class LogIn(Menu):
    def __init__(self):
        super().__init__("login")

    def entrada(self):
        salir = False
        while not salir:
            self.mostrar()
            usuario = input("Ingresse usuario: ")
            self.mostrar(usuario)
            password = input("Ingrese contrasena: ")
            self.mostrar(usuario, password)
            if (usuario != "") or (password != ""):
                with open("usuarios.csv", "r", encoding="utf8") as usuarios:
                    for user in usuarios:
                        user = user.strip()
                        if (usuario in user.split(",")[1]) and (password in user.split(",")[2]):
                            return user.split(",")[0]
                    usuarios.close()
                return "."
            else:
                return "."

    def mostrar(self, usuario="", contraseña=""):
        centro = 60
        mensaje = "\n" + " inicio de sesion ".title().center(centro, "=") + "\n"
        mensaje += "Usuario: {0}".format(usuario).ljust(centro) + "\n"
        mensaje += "Contraseña: {0}".format("*" * len(contraseña)).ljust(centro) + "\n"
        mensaje += "".center(centro, "=") + "\n"
        frame(mensaje)
        pass


class Diccionario(Menu):
    def __init__(self, nombre, opciones):
        super().__init__(nombre, opciones)
        pass

    def mostrar(self):
        salir = False
        while not salir:
            mensaje = ""
            diccionario = {}
            for number in range(len(self.opciones)):
                mensaje += "{}. {}\n".format(number, self.opciones[str(number)])
            print("estado del diccionario: \n".title())
            for key, value in diccionario.items():
                print("{} = {}\n".format(key, value))
            print("Elegir opcion: \n")
            print(mensaje + "\n Otra entrada para salir o terminar...")
            respuesta = input("Respuesta: ")
            if respuesta in self.opciones:
                valor = input("Ingrese valor: ")
                diccionario[self.opciones[respuesta]] = valor
            else:
                salir = True
            frame()
        if len(diccionario) == len(self.opciones):
            return diccionario
        else:
            return {}

    def entrada(self):
        pass


class Basico(Menu):
    def __init__(self, nombre, opciones):
        super().__init__(nombre, opciones)
        pass

    def entrada(self):
        pass

    def mostrar(self):
        salir = False
        while not salir:
            mensaje = ""
            for number in range(len(self.opciones)):
                mensaje += "{}. {}\n".format(str(number), str(self.opciones[str(number)]))
            print("Elegir opcion: \n")
            print(mensaje + "Otra entrada para salir o anular...")
            respuesta = input("Respuesta: ")
            if respuesta in self.opciones:
                return self.opciones[respuesta]
            else:
                salir = True
            frame()


class Principal(Menu):
    def __init__(self, nombre, usuarioActivo, fechaActual, opciones):
        super().__init__(nombre, opciones)
        self.usuario = usuarioActivo
        self.fecha = fechaActual

    def entrada(self, salir):
        self.mostrar()
        entrada = input("Respuesta: ")
        if entrada in self.opciones:
            if entrada == "x":
                salir = self.opciones[entrada]()
            elif entrada == "f":
                self.opciones[entrada](input("Ingrese la fecha en formato A*-MM-DD: "))
            else:
                self.opciones[entrada]()
        frame()
        return salir

    def mostrar(self):
        if self.usuario.recurso_id is "":
            print("Elija una accion:\n1. Crear usuario\n2. Agregar pronostico del clima\n3. Agregar incendio\n4. "
                  "Consulta avanzada\n5. Consulta basica\n6. Leer base de datos\nf. Cambiar fecha\nx. Cerrar sesion")
        else:
            pass
