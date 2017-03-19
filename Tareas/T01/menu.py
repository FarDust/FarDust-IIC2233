# Menu v1.0.1

from abc import ABCMeta, abstractmethod
from dibujar import frame


class Menu(metaclass=ABCMeta):
    def __init__(self, nombre, opciones=None):
        if opciones is None:
            opciones = []
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
            if(usuario == "") or (password == ""):
                with open("usuarios.csv", "r", encoding="utf8") as usuarios:
                    for user in usuarios:
                        user = user.strip()
                        print(user.split(","))
                        if (usuario in user.split(",")[1]) and (password in user.split(",")[2]):
                            return user.split(",")[0]
                    usuarios.close()
                return "."
            else:
                return "."

    def mostrar(self, usuario="", contraseña=""):
        centro = 60
        mensaje = "\n" +" inicio de sesion ".title().center(centro,"=") + "\n"
        mensaje += "Usuario: {0}".format(usuario).ljust(centro) + "\n"
        mensaje += "Contraseña: {0}".format("*" * len(contraseña)).ljust(centro) + "\n"
        mensaje += "".center(centro,"=") + "\n"
        frame(mensaje)
        pass
