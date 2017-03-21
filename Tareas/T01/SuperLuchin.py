# SuperLuchín Alpha v1.0.0

from menu import LogIn, Principal
from leer import Users, Resources, Fire
from usuarios import Terreno, Anaf
from comprobar import comprobar_fecha
from datos import Recurso,Incendio


class Fecha:
    def __init__(self):
        self.fecha = "1-01-01"

    def cambiar(self, fecha):
        if comprobar_fecha(fecha):
            temp = fecha.split("-")
            temp[1].rjust(2, "0")
            temp[2].rjust(2, "0")
            self.fecha = "-".join(temp)
            temp.clear()
        else:
            self.cambiar(input("Ingrese la fecha en formato A*-MM-DD: "))


if __name__ == '__main__':
    salir = False
    iniciSesion = False
    iniciar = LogIn()
    opciones = {"": iniciar.entrada}
    rutaDeUsuarios = Users()
    fechaActual = Fecha()
    recursos = {}
    incendios = {}
    # Instanciar recursos
    for key, value in Resources().leer.items():
        recursos[key] = Recurso(**value)

    # Instanciar incendios
    for key, value in Fire().leer.items():
        recursos[key] = Incendio(**value)


    while not salir:
        print("Iniciar sesion:".title())
        print("ENTER para Iniciar sesion\nCualquier otro para salir")
        eleccion = input("Respuesta: ")
        if eleccion in opciones:
            usuarioActual = opciones[eleccion]()
            if usuarioActual != "." and usuarioActual is not None:
                if rutaDeUsuarios.completar(usuarioActual)["recurso_id"] == "":
                    usuarioActivo = Anaf(rutaDeUsuarios.completar(usuarioActual))
                    opciones = {"1": usuarioActivo.crear_usuario,
                                "2": usuarioActivo.agregar_pronostico,
                                "3": usuarioActivo.agregar_incendio,
                                "4": usuarioActivo.consulta_avanzada,
                                "5": usuarioActivo.consulta_basica,
                                "f": fechaActual.cambiar,
                                "6": usuarioActivo.leer_base,
                                "x": usuarioActivo.cerrar_sesion}
                else:
                    usuarioActivo = Terreno(rutaDeUsuarios.completar(usuarioActual))
                    opciones = {"1": usuarioActivo.crear_usuario,
                                "2": usuarioActivo.consulta_avanzada,
                                "3": usuarioActivo.consulta_basica,
                                "4": fechaActual.cambiar,
                                "x": usuarioActivo.cerrar_sesion}
                salir2 = False
                fechaActual.cambiar(input("Ingrese la fecha en formato A*-MM-DD: "))
                menu = Principal("main", usuarioActivo, fechaActual, opciones)
                while not salir2:
                    print(fechaActual.fecha.center(60, "="))
                    if usuarioActivo.recurso_id != "":
                        # Barra de estado aqui
                        pass
                    salir2 = menu.entrada(salir2)
            else:
                print("Usuario no esta en la base de datos!!!\n")
        else:
            salir = True
