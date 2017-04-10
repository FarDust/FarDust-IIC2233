from super_lista import Lista
from diccionario import Posicionado
from os import mkdir


# Esta clase es parte de un objeto pais, pero tiene conttrol casi absoluto del pais asi que lo resive como argumento
# Se puede asumir como un complemento al estado soberano
class Gobierno:
    def __init__(self, pais, fronteras):
        self.pais = pais
        self.fronteras = fronteras
        self.prioridades = Lista()  # La superlista actua como lista, pila y cola a la vez :)
        self.acciones = Posicionado(self.cerrar_aeropuerto, 0.8,
                                    self.cerrar_fronteras, self.prioridad_fronteras,
                                    self.entregar_mascarillas, 0.5,
                                    self.desbloquear_rutas, 0.7)

    @property
    def prioridad_fronteras(self):
        try:
            suma = 0
            for frontera in self.fronteras:
                if frontera.pais_a == self.pais.nombre:
                    suma += frontera.statics_b
                else:
                    suma += frontera.statics_a
            return (suma / len(self.pais.fronteras)) / 100
        except ZeroDivisionError:
            return 0.0

    def prioridad(self, accion):
        return (self.acciones[accion] * self.pais.poblacion.infectados) / self.pais.poblacion.total

    def evaluar(self):
        priority = Lista()
        re_list = Lista()
        n = 0
        for accion in self.acciones.keys():
            if n == 0 and (
                            self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25) and \
                            self.pais.aeropuerto.abierto is True:
                i = self.prioridad(accion)
            elif n == 1 and (
                            self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20) and \
                    self.pais.frontera is False:
                i = self.prioridad(accion)
            elif n == 2 and self.pais.poblacion.per_infectados > ((1 / 3) * 100) and self.pais.mascarillas is False:
                i = self.prioridad(accion)
            elif n == 3 and ((self.pais.aeropuerto.abierto is False and self.noticias > 4 and not (
                            self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25)) or (
                            self.pais.frontera is False and not (
                                    self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20))):
                i = self.prioridad(accion)
            else:
                i = 0.0
            if n == 3 and self.pais.cura is True:
                i = 1.0
            priority.append(i)
            n += 1
        for i in range(len(priority)):
            if priority[i] > 0.0:
                re_list.append(Lista(priority[i], self.acciones.keys()[i]))
        re_list = Lista(*sorted(re_list, key=lambda x: x[0], reverse=True))
        return re_list

    def entregar_mascarillas(self):
        self.pais.mascarillas = True
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("{} entrego mascarillas a sus ciudadanos\n".format(self.pais.nombre))

    def cerrar_aeropuerto(self):
        self.pais.aeropuerto.abierto = False
        for vuelo in self.pais.aeropuerto.vuelos:
            if self.pais.nombre == vuelo.f_pais_a:
                vuelo.f_pais_a = False
            else:
                vuelo.f_pais_b = False
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("{} decide cerrar todos sus aeropuertos\n".format(self.pais.nombre))
            sucesos.write("{}\n".format(self.pais))

    def cerrar_fronteras(self):
        self.pais.frontera = False
        for frontera in self.pais.fronteras:
            if self.pais.nombre == frontera.f_pais_a:
                frontera.f_pais_a = False
            else:
                frontera.f_pais_b = False
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("{} decide cerrar todas sus fronteras\n".format(self.pais.nombre))
            sucesos.write("{}\n".format(self.pais))

    def desbloquear_rutas(self):
        if self.noticias > 4 and not (self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25):
            self.abrir_aeropuerto()
        if not (self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20) and \
                not self.pais.frontera:
            self.abrir_fronteras()
        elif self.pais.cura:
            self.abrir_aeropuerto()
            self.abrir_fronteras()

    def noticias_infeccion(self, datos):
        self.noticias = datos

    def abrir_aeropuerto(self):
        self.pais.aeropuerto.abierto = True
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("{} abrio su aeropuerto\n".format(self.pais.nombre))
            sucesos.write("{}".format(self.pais))

    def abrir_fronteras(self):
        self.pais.frontera = True
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("{} restablecio sus conexiones terrestres con otros paises\n".format(self.pais.nombre))
            sucesos.write("{}\n".format(self.pais))
