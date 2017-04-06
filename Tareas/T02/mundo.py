from super_lista import Lista
from gobierno import Gobierno
from random import choice, randint, random


class Poblacion:
    def __init__(self, poblacion=0):
        self.limpios = int(poblacion)
        self.infectados = 0
        self.muertos = 0

    def infectar(self, n=1):
        if n > self.limpios:
            n = self.limpios
        self.infectados += n
        self.limpios -= n

    def matar(self, n):
        if n > self.infectados:
            n = self.infectados
        self.muertos += n
        self.infectados -=n

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
            self.mascarillas = False
            self.cura = False
            # Encargado del manejo de entrada infeccion
            self.frontera = True

    def add_vertex(self, frontera):
        self.fronteras.append(frontera)

    def actualizar_datos(self):
        if self.poblacion.infectados > 0:
            self.expandir()
        for frontera in self.fronteras:
            if frontera.pais_a == self.nombre:
                frontera.statics_a = self.poblacion.per_infectados
            else:
                frontera.statics_b = self.poblacion.per_infectados
        if not self.frontera:
            for frontera in self.fronteras:
                if frontera.pais_a == self.nombre:
                    frontera.f_pais_a = False
                else:
                    frontera.f_pais_b = False
        if not self.aeropuerto.abierto:
            for ruta in self.aeropuerto.vuelos:
                ruta.abierto = False

    def expandir(self):
        if self.poblacion.per_infectados > 5:
            infectados = randint(0, self.grandes_numeros)
            if self.mascarillas:
                infectados = int(infectados*0.3)
            self.poblacion.infectar(infectados)
        else:
            for i in range(self.poblacion.infectados):
                infectados = randint(0, 6)
                if self.mascarillas:
                    infectados = int(infectados * 0.3)
                self.poblacion.infectar(infectados)
        print("En {} hay infectados {}".format(self.nombre, self.poblacion.infectados))
        print(self.poblacion)

    def calcular_muertos(self, probabilidad):
        n = 0
        for i in range(int(self.poblacion.infectados * 0.01)):
            if random() < probabilidad:
                n += int(self.poblacion.infectados * 0.01)
        self.poblacion.matar(n)

    @property
    def grandes_numeros(self):
        return 6 * max(int(self.poblacion.infectados), 1)

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
        return "{}: {}".format(self.nombre, self.fronteras + self.aeropuerto.vuelos)


class Mundo:
    def __init__(self, mundo=None, enfermedad=None):
        if mundo is None:
            self.mundo = Lista()
        self.mundo = mundo
        self.sugerencias = Lista()
        self.dias = 0
        self.enfermedad = enfermedad
        choice(self.mundo).poblacion.infectar()
        self.enfermedad_detectada = False
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

    @property
    def per_infeccion(self):
        return round((self.poblacion_infectada / self.poblacion_mundial) * 100, 2)

    @property
    def probabilidad_muerte(self):
        return min(min(0.2, self.dias**2/100000)*self.enfermedad.mortalidad, 1)

    def actualizar(self):
        for pais in self.mundo:
            pais.actualizar_datos()
            pais.calcular_muertos(self.probabilidad_muerte)
            pais.gobierno.noticias_infeccion(self.per_infeccion)
            # Convertir en cola de verdad
            self.sugerencias += pais.gobierno.evaluar()
            self.sugerencias = Lista(*sorted(self.sugerencias, key=lambda x: x[0], reverse=True))
        print(self.sugerencias)
        print(self.per_infeccion, "%")
        for i in range(3):
            if len(self.sugerencias) > 0:
                self.sugerencias.popleft()[1]()
        self.dias += 1

    def __repr__(self):
        visitados = Lista()
        for pais in self.mundo:
            pass
