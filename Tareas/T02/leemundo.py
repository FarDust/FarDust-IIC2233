from connections_generator import generate_connections
from super_lista import Lista
from mundo import Poblacion, Pais
from Insfrastructuras import Frontera, Aeropuerto, RutaDeVuelo


class Leer:
    # Devuelve una lista con todos los paises instancias y con sus respectivas poblaciones
    def generar_paises(self):
        world = Lista()
        with open("population.csv", "r", encoding="utf8") as paises:
            countries = Lista(*paises.readlines())
            try:
                n_paises = Lista(*countries[0].strip().split(",")).index("Pais")
                n_poblacion = Lista(*countries[0].strip().split(",")).index("Poblacion")
                countries.popleft()
            except IndexError:
                n_paises = 0
                n_poblacion = 1
            for pais in countries:
                pais = pais.strip().split(",")
                world.append(Pais(pais[n_paises], Poblacion(pais[n_poblacion])))
            paises.close()
        return world

    # Conecta un mundo por via terrestre (el Mundo a insgresar debe ser de clase Lista())
    # Instancia las fronteras y las agrega a sus respectivos paises(cada frontera se agrega a 2 paises)
    # Retorna el mundo conectado
    def generar_fronteras(self, world=None):
        if not world:
            world = Lista()
        if len(world) == 0:
            world = self.generar_paises()
        fronteiras = Lista()
        with open("borders.csv", "r", encoding="utf8") as fronteras:
            borders = Lista(*fronteras.readlines())
            for border in range(len(borders) - 1):
                fronteiras.append(Frontera(*borders[border + 1].strip().split(";")))
            fronteras.close()
        for fronteira in fronteiras:
            if Pais(fronteira.pais_a, Poblacion()) in world:
                if fronteira not in world[world.index(Pais(fronteira.pais_a, Poblacion()))].fronteras:
                    world[world.index(Pais(fronteira.pais_a, Poblacion()))].fronteras.append(fronteira)
            if Pais(fronteira.pais_b, Poblacion()) in world:
                if fronteira not in world[world.index(Pais(fronteira.pais_b, Poblacion()))].fronteras:
                    world[world.index(Pais(fronteira.pais_b, Poblacion()))].fronteras.append(fronteira)
        return world

    def generar_aeropuertos(self, world=None):
        if not world:
            world = Lista()
        if len(world) == 0:
            world = self.generar_fronteras()
        generate_connections()
        with open("random_airports.csv", "r", encoding="utf8") as rutas:
            paths = Lista(*rutas.readlines())
            paths.popleft()
            aeropuertos = Lista()
            for path in paths:
                if Lista(*path.strip().split(","))[0] not in aeropuertos:
                    aeropuertos.append(Lista(*path.strip().split(","))[0])
                if Lista(*path.strip().split(","))[1] not in aeropuertos:
                    aeropuertos.append(Lista(*path.strip().split(","))[1])
            for aeropuerto in aeropuertos:
                if Pais(aeropuerto, Poblacion()) in world:
                    world[world.index(Pais(aeropuerto, Poblacion()))].aeropuerto = Aeropuerto()
            rutas.close()
        return self.__generar_rutas_aereas(world)

    def __generar_rutas_aereas(self, world):
        rotas = Lista()
        with open("random_airports.csv", "r", encoding="utf8") as rutas:
            paths = Lista(*rutas.readlines())
            for path in range(len(paths) - 1):
                rotas.append(RutaDeVuelo(*paths[path + 1].strip().split(",")))
            rutas.close()
        for rota in rotas:
            if Pais(rota.pais_a, Poblacion()) in world:
                if rota not in world[world.index(Pais(rota.pais_a, Poblacion()))].aeropuerto.vuelos:
                    world[world.index(Pais(rota.pais_a, Poblacion()))].aeropuerto.vuelos.append(rota)
            if Pais(rota.pais_b, Poblacion()) in world:
                if rota not in world[world.index(Pais(rota.pais_b, Poblacion()))].aeropuerto.vuelos:
                    world[world.index(Pais(rota.pais_b, Poblacion()))].aeropuerto.vuelos.append(rota)
        return world


def generar_paises():
    return Leer().generar_paises()


def generar_fronteras(world=None):
    return Leer().generar_fronteras(world)


def generar_aeropuertos(world=None):
    return Leer().generar_aeropuertos(world)
