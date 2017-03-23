# PRIMERA PARTE: Estructura basica
class Nodle:
    def __init__(self, valor=None):
        self.valor = valor
        self.siguiente = None


class Principia:
    def __init__(self):
        self.ultimo = None
        self.primero = None
        self.cantidad_nodles = 0

    def agregar_nodle(self, value):
        if not self.primero:
            self.primero = Nodle(value)
            self.ultimo = self.primero
        else:
            self.ultimo.siguiente = Nodle(value)
            self.ultimo = self.ultimo.siguiente
        self.cantidad_nodles += 1

    def buscar_nodle(self, value, contador=0, nodo=None):
        if contador is 0:
            nodo = self.ultimo
        if nodo.valor == value:
            return True
        elif contador == self.cantidad_nodles:
            return False
        else:
            return self.buscar_nodle(value, contador + 1, nodo.siguiente)

    def obtener(self, pos):
        nodle = self.primero
        for i in range(pos):
            if nodle:
                nodle = nodle.siguiente
        if not nodle:
            raise IndexError
        else:
            return nodle.valor

    def __repr__(self):
        principia = ""
        contador = 0
        nodo_actual = self.ultimo
        while contador != self.cantidad_nodles:
            principia += "{}>".format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
            contador += 1
        principia.strip(">")


# SEGUNDA PARTE: Clase Isla
class Isla:
    def __init__(self,nombre):
        self.nombre = nombre
        self.conexiones = Principia()

    def __repr__(self):
        rep = ""
        for i in range(self.conexiones.cantidad_nodles):
            rep += "{} --> {}\n".format(self.nombre,self.conexiones.obtener(i))
        return rep

    def __eq__(self, other):
        if self.nombre == other.nombre:
            return True
        else:
            return False


# TERCERA PARTE: Clase Archipielago
class Archipielago:
    def __init__(self):
        self.islas = Principia()

    def __repr__(self):

        pass

    def agregar_isla(self, nombre):
        self.islas.agregar_nodle(Isla(nombre))
        pass

    def conectadas(self, nombre_origen, nombre_destino):

        pass

    def agregar_conexion(self, nombre_origen, nombre_destino):
        if not self.islas.buscar_nodle(Isla(nombre_destino)):
            self.islas.agregar_nodle(Isla(nombre_destino))
        if not self.islas.buscar_nodle(Isla(nombre_origen)):
            self.islas.agregar_nodle(Isla(nombre_origen))
        else:
            self.islas.obtener(i).conexiones.agregar_nodle(Isla(nombre_destino))

    def construir(self, archivo):
        
        pass

    def propagacion(self, nombre_origen):

        pass


if __name__ == '__main__':
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")  # Instancia y construye
    print(arch)  # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    print(arch.propagacion("Pasesterot"))
    print(arch.propagacion("Cartonat"))
    print(arch.propagacion("Womeston"))
