from super_lista import Lista
from gobierno import Gobierno


class Poblacion:
    def __init__(self, poblacion=0):
        self.limpios = int(poblacion)
        self.infectados = 0
        self.muertos = 0

    @property
    def total(self):
        return self.limpios + self.infectados + self.muertos

    @property
    def per_infectados(self):
        return round((self.infectados / self.total) * 100, 2)

    @property
    def per_limpios(self):
        return round((self.limpios / self.total) * 100, 2)

    @property
    def per_muertos(self):
        return round((self.muertos / self.total) * 100, 2)

    def __repr__(self):
        return "Sanos: {}%,Infectados: {}%,Muertos: {}%".format(self.per_limpios, self.per_infectados, self.per_muertos)


class Pais:
    def __init__(self, nombre, poblacion):
        self.nombre = nombre
        self.poblacion = poblacion
        if poblacion.total > 0:
            self.fronteras = Lista()
            self.aeropuerto = None
            self.gobierno = Gobierno(self, self.fronteras)

    def add_vertex(self, frontera):
        self.fronteras.append(frontera)

    def actualizar_datos(self):
        for frontera in self.fronteras:
            if frontera.pais_a == self.nombre:
                frontera.statics_a = self.poblacion.per_infectados
            else:
                frontera.statics_b = self.poblacion.per_infectados

    @property
    def conection_number_e(self):
        return len(self.fronteras)

    @property
    def conection_number_a(self):
        return len(self.aeropuerto.vuelos)

    def __eq__(self, other):
        if self.nombre == other.nombre:
            return True
        else:
            return False

    def __repr__(self):
        temp = Lista()
        return "{}: {}".format(self.nombre, self.fronteras + self.aeropuerto.vuelos)


class Mundo:
    def __init__(self, mundo=None):
        if mundo is None:
            self.mundo = Lista()
        self.mundo = mundo
        self.sugerencias = Lista()
        self.actualizar()

    @property
    def poblacion_mundial(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.total
        return total

    @property
    def poblacion_infectada(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.infectados
        return total

    @property
    def poblacion_limpia(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.limpios
        return total

    @property
    def poblacion_muerta(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.muertos
        return total

    def actualizar(self):
        print(self.poblacion_mundial)
        for pais in self.mundo:
            pais.actualizar_datos()
            self.sugerencias += pais.gobierno.evaluar()
            self.sugerencias = Lista(*sorted(self.sugerencias, key=lambda x: x[0], reverse=True))
        for i in range(3):
            if len(self.sugerencias) > 0:
                self.sugerencias.popleft()[1]()

    def __repr__(self):
        visitados = Lista()
        for pais in self.mundo:
            pass
