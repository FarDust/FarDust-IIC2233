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

    def buscar_nodle_old(self, value, contador=0, nodo=None):
        print("recursion {}".format(contador))
        if contador == 0:
            nodo = self.ultimo
        if self.ultimo is None and self.primero is None:
            return False
        elif nodo.valor == value:
            return True
        elif contador == self.cantidad_nodles:
            return False
        else:
            return self.buscar_nodle(value, contador + 1, nodo.siguiente)

    def buscar_nodle(self, value):
        for i in range(self.cantidad_nodles):
            if self.obtener(i) == value:
                return True
        return False

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
        nodo_actual = self.primero
        while nodo_actual:
            principia += "{}>".format(nodo_actual.valor)
            nodo_actual = nodo_actual.siguiente
            contador += 1
        principia.strip(">")
        return principia


# SEGUNDA PARTE: Clase Isla
class Isla:
    def __init__(self, nombre):
        self.nombre = nombre
        self.conexiones = Principia()

    def __repr__(self):
        rep = self.nombre+ "\n"
        for i in range(self.conexiones.cantidad_nodles):
            rep += "{} --> {}\n".format(self.nombre, self.conexiones.obtener(i))
        return rep

    def __eq__(self, other):
        if self.nombre == other.nombre:
            return True
        else:
            return False


# TERCERA PARTE: Clase Archipielago
class Archipielago:
    def __init__(self, archivo):
        self.islas = Principia()
        self.construir(archivo)

    def __repr__(self):
        string = ""
        for i in range(self.islas.cantidad_nodles):
            string+= "{}".format(self.islas.obtener(i).conexiones)
        return string
        pass

    def agregar_isla(self, nombre):
        self.islas.agregar_nodle(Isla(nombre))
        pass

    def conectadas(self, nombre_origen, nombre_destino):
        if self.islas.buscar_nodle(Isla(nombre_origen)) and self.islas.buscar_nodle(Isla(nombre_destino)):
            for i in range(self.islas.cantidad_nodles):
                if self.islas.obtener(i) is Isla(nombre_origen):
                    if self.islas.obtener(i).conexiones.buscar_nodle(Isla(nombre_destino)):
                        return True
                    else:
                        return False
                else:
                    return False
        else:
            return False

    def agregar_conexion(self, nombre_origen, nombre_destino):
        if not self.islas.buscar_nodle(Isla(nombre_destino)):
            self.islas.agregar_nodle(Isla(nombre_destino))
        if not self.islas.buscar_nodle(Isla(nombre_origen)):
            self.islas.agregar_nodle(Isla(nombre_origen))
        else:
            for i in range(self.islas.cantidad_nodles):
                if self.islas.obtener(i).nombre == nombre_origen:
                    for j in range(self.islas.obtener(i).conexiones.cantidad_nodles):
                        if self.islas.obtener(i).conexiones.obetener(j).nombre == nombre_destino:
                            self.islas.obtener(i).conexiones.agregar_nodle(self.islas.obtener(i).conexiones.obetener(j))
        pass

    def construir(self, archivo):
        with open(archivo, "r") as mapa:
            for linea in mapa:
                linea = linea.strip()
                nombre_origen = linea.split(",")[0]
                nombre_destino = linea.split(",")[1]
                self.agregar_conexion(nombre_origen, nombre_destino)
            mapa.close()

        pass

    def propagacion(self, nombre_origen, infectadas=None):
        if infectadas is None:
            infectadas = Principia()
        for i in range(self.islas.cantidad_nodles):
            if self.islas.obtener(i) is Isla(nombre_origen):
                infectadas.agregar_nodle(self.islas.obtener(i))
                if self.islas.obtener(i).conexiones.cantidad_nodles is 0:
                    return
                else:
                    for j in range(self.islas.obtener(i).conexiones.cantidad_nodles):
                        self.propagacion(self.islas.obtener(i).conexiones.obetener(j).nombre, infectadas)
        return infectadas


if __name__ == '__main__':
    # No modificar desde esta linea
    # (puedes comentar lo que no este funcionando aun)
    arch = Archipielago("mapa.txt")  # Instancia y construye
    print(arch)  # Imprime el Archipielago de una forma que se pueda entender
    print(arch.propagacion("Perresus"))
    print(arch.propagacion("Pasesterot"))
    print(arch.propagacion("Cartonat"))
    print(arch.propagacion("Womeston"))
