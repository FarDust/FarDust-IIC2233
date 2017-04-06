from super_lista import Lista
from diccionario import Posicionado


# Esta clase es parte de un objeto pais, pero tiene conttrol casi absoluto del pais asi que lo resive como argumento
# Se puede asumir como un complemento al estado soberano
class Gobierno:
    def __init__(self, pais, fronteras):
        self.pais = pais
        self.fronteras = fronteras
        self.mascarillas = False
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
            i = self.prioridad(accion)
            if n == 1 and (not(self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20)
                    or self.pais.frontera is False):
                i = 0.0
            if n == 0 and (not(self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25)
                           or (self.pais.aeropuerto.abierto is False or not (self.noticias > 4))):
                i = 0.0
            if n == 2 and (not (self.pais.poblacion.per_infectados > ((1 / 3) * 100)) or self.pais.mascarillas is True):
                i = 0.0
            if n == 3 and ((self.pais.aeropuerto.abierto is True or
                                (self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25)) or
                          (self.pais.frontera is True or (
                                self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20))):
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
        print("{} entrego mascarillas a sus ciudadanos".format(self.pais.nombre))

    def cerrar_aeropuerto(self):
        self.pais.aeropuerto.abierto = False
        print("{} decide cerrar todos sus aeropuertos".format(self.pais.nombre))

    def cerrar_fronteras(self):
        self.pais.frontera = False
        raise SystemExit
        print("{} decide cerrar todas sus fronteras".format(self.pais.nombre))

    def desbloquear_rutas(self):
        if self.noticias > 4 and not (self.pais.poblacion.per_infectados > 50 or self.pais.poblacion.per_muertos > 25):
            self.abrir_aeropuerto()
            print("{} abrio su aeropuerto".format(self.pais.nombre))
        if not (self.pais.poblacion.per_infectados > 80 or self.pais.poblacion.per_muertos > 20) and\
                not self.pais.frontera:
            self.abrir_fronteras()
            print("{} restablecio sus conexiones terrestres con otros paises".format(self.pais.nombre))

    def noticias_infeccion(self, datos):
        self.noticias = datos

    def abrir_aeropuerto(self):
        self.pais.aeropuerto.abierto = True

    def abrir_fronteras(self):
        self.pais.frontera = True
