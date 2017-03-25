# SuperLuchín Alpha v1.0.0

from menu import LogIn, Principal
from leer import Users, Resources, Fire, Meteorology
from usuarios import Terreno, Anaf
from comprobar import comprobar_fecha
from datos import Recurso, Incendio, Meteorologia
from dibujar import frame
from estrategia import EstrategiaDeExtincion


class Fecha:
    def __init__(self):
        self.fecha = "1-01-01 00:00:00"

    def cambiar(self, fecha):
        if comprobar_fecha(fecha):
            temp = fecha.split(" ")[0].split("-")
            temp[1] = temp[1].rjust(2, "0")
            temp[2] = temp[2].rjust(2, "0")
            actual = "-".join(temp)
            temp = fecha.split(" ")[1].split(":")
            temp[1] = temp[1].rjust(2, "0")
            temp[2] = temp[2].rjust(2, "0")
            hora = ":".join(temp)
            self.fecha = actual + " " + hora
            temp.clear()
        else:
            self.cambiar(input("Ingrese la fecha en formato A*-MM-DD HH:MM:SS : "))


def incendios_activos():
    frame()
    print("Incendios activos")
    for value in incendios.values():
        if value.puntos_poder > 0:
            print(value)
    input("Enter para continuar...")


def incendios_apagados():
    frame()
    print("Incendios activos")
    for value in incendios.values():
        if value.puntos_poder <= 0:
            print("Incendio: {} |Fecha apagado: {}|"
                  "Fecha de inicio: {}|Recursos: {} ".format(value.id, value.fecha_apagado, value.fecha_inicio,
                                                             value.recursos))
    input("Enter para continuar...")


def acceso_base_terreno():
    frame()
    incendio = recursos[usuarioActivo.recurso_id].incendio
    for key, value in Fire().leer[incendio.id].items():
        print("{}: {}".format(key, value), end="\n")
    print(
        "Porcentaje de extincion: {}, Recursos asignados: {}".format(incendio.porcentaje_extincion, incendio.recursos))
    print("Enter para continuar...")


def recursos_utilizados():
    temp = []
    for recurso in recursos.values():
        temp.append(recurso)
    temp.sort()
    temp = temp[::-1]
    for recurso in temp:
        print("RecursoID: {}|Coeficiente de uso: {}".format(recurso.id, recurso.coeficiente_uso))


def recursos_efectivos():
    temp = {}
    for value in recursos.values():
        temp[value.coeficiente_eficiencia] = value
    h = sorted(temp)[::-1]
    for recurso in h:
        print("RecursoID: {}|Coeficiente de eficiencia: {}".format(recurso.id, recurso.coeficiente_eficiencia))


if __name__ == '__main__':
    salir = False
    iniciSesion = False
    iniciar = LogIn()
    opciones = {"": iniciar.entrada}
    rutaDeUsuarios = Users()
    fechaActual = Fecha()
    recursos = {}
    incendios = {}
    climas = {}

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
                                "f": fechaActual.cambiar,
                                "4": usuarioActivo.leer_base,
                                "5": incendios_activos,
                                "6": incendios_apagados,
                                "7": recursos_utilizados,
                                "8": recursos_efectivos,
                                "9": EstrategiaDeExtincion().menu(),
                                "x": usuarioActivo.cerrar_sesion}
                else:
                    usuarioActivo = Terreno(rutaDeUsuarios.completar(usuarioActual))
                    opciones = {"f": fechaActual.cambiar,
                                "x": usuarioActivo.cerrar_sesion}
                salir2 = False
                fechaActual.cambiar(input("Ingrese la fecha en formato A*-MM-DD HH:MM:SS : "))
                menu = Principal("main", usuarioActivo, fechaActual, opciones)
                # Instanciar recursos
                for key, value in Resources().leer.items():
                    recursos[key] = Recurso(**value)

                # Instanciar incendios
                for key, value in Fire().leer.items():
                    incendios[key] = Incendio(fecha=fechaActual.fecha, **value)

                # Instaciar climas
                for key, value in Meteorology().leer.items():
                    climas[key] = Meteorologia(**value)

                while not salir2:
                    print(fechaActual.fecha.center(60, "="))
                    if usuarioActivo.recurso_id != "":
                        if recursos[usuarioActivo.recurso_id].incendio:
                            opciones["1"] = acceso_base_terreno
                        for key, value in Resources().leer[usuarioActivo.recurso_id].items():
                            print("{}: {}|".format(key, value), end="")
                        print(recursos[usuarioActivo.recurso_id])
                        pass
                    salir2 = menu.entrada(salir2)
            else:
                print("Usuario no esta en la base de datos!!!\n")
        else:
            salir = True
