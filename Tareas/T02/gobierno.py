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
                                    self.abrir_aeropuerto, 0.7,
                                    self.abrir_fronteras, 0.7)

    @property
    def prioridad_fronteras(self):
        try:
            suma = 0
            for frontera in self.fronteras:
                if frontera.pais_a == self.pais.nombre:
                    suma += frontera.statics_b
                else:
                    suma += frontera.statics_a
            return (suma / len(self.fronteras)) / 100
        except ZeroDivisionError:
            return 0.0

    def prioridad(self, accion):
        return (self.acciones[accion] * self.pais.poblacion.infectados) / self.pais.poblacion.total

    def evaluar(self):
        priority = Lista()
        re_list = Lista()
        for accion in self.acciones.keys():
            priority.append(self.prioridad(accion))
        for i in range(len(priority)):
            if priority[i] > 0.0:
                re_list.append(Lista(priority[i], self.acciones.keys()[i]))
        re_list = Lista(*sorted(re_list, key=lambda x: x[0], reverse=True))
        return re_list

    def entregar_mascarillas(self):
        pass

    def cerrar_aeropuerto(self):
        pass

    def cerrar_fronteras(self):
        pass

    def abrir_aeropuerto(self):
        pass

    def abrir_fronteras(self):
        pass
