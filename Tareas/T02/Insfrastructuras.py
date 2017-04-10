from super_lista import Lista


class Insfrastructura:
    def __init__(self, abierto=True):
        self.abierto = abierto


class Aeropuerto(Insfrastructura):
    estados = Lista("limpio", "infectado", "muerto")

    def __init__(self, *args):
        super().__init__(abierto=False)
        self.vuelos = Lista()
        self.estado = self.estados[0]

    def agregar_ruta(self, ruta):
        self.vuelos.append(ruta)

    def __repr__(self):
        return "{}".format(self.vuelos)


class Frontera(Insfrastructura):
    # Al crearse este objeto se guardara en los dos paises vecinos a la vez
    def __init__(self, *args):
        super().__init__()
        args = Lista(*args)
        self.pais_a = args[0]
        self.pais_b = args[1]
        self.statics_a = 0
        self.statics_b = 0
        self.f_pais_a = True
        self.f_pais_b = True
        self.pais_a_o = None
        self.pais_b_o = None

    def guardar(self):
        with open("current/{}_{}_f.csv".format(self.pais_a, self.pais_b), "w") as archivo:
            archivo.write("{},{},{},{}".format(self.statics_a, self.statics_b, self.f_pais_a, self.f_pais_b))

    def cargar(self):
        with open("current/{}_{}_f.csv".format(self.pais_a, self.pais_b), "r") as archivo:
            linea = Lista(*Lista(*archivo.readlines())[0].strip().split(","))
            self.statics_a = float(linea[0])
            self.statics_b = float(linea[1])
            self.f_pais_a = "True" is linea[2]
            self.f_pais_b = "True" is linea[3]

    @property
    def abierto(self):
        if self.f_pais_a and self.f_pais_b:
            return True
        else:
            return False

    @abierto.setter
    def abierto(self, bool):
        if type(bool) is type(True):
            self.f_pais_b = bool
            self.f_pais_a = bool
        else:
            raise ValueError

    def __eq__(self, other):
        if self.pais_a == other.pais_a and self.pais_b == other.pais_b:
            return True
        elif self.pais_b == other.pais_a and self.pais_a == other.pais_b:
            return True
        else:
            return False

    def __repr__(self):
        if self.abierto:
            conexion = "<->"
        else:
            conexion = "| / |"
        return "{} {} {}".format(self.pais_a, conexion, self.pais_b)


class RutaDeVuelo(Frontera):
    def __init__(self, *args):
        args = Lista(*args)
        super().__init__(*args)
        self.pais_a = args[0]
        self.pais_b = args[1]
        self.statics_a = 0
        self.statics_b = 0
        self.f_pais_a = True
        self.f_pais_b = True
        self.abierto = False

    def guardar(self):
        with open("current/{}_{}_v.csv".format(self.pais_a, self.pais_b), "w") as archivo:
            archivo.write("{},{},{},{}".format(self.statics_a, self.statics_b, self.f_pais_a, self.f_pais_b))

    def cargar(self):
        with open("current/{}_{}_v.csv".format(self.pais_a, self.pais_b), "r") as archivo:
            linea = Lista(*Lista(*archivo.readlines())[0].strip().split(","))
            self.statics_a = float(linea[0])
            self.statics_b = float(linea[1])
            self.f_pais_a = "True" is linea[2]
            self.f_pais_b = "True" is linea[3]

    @property
    def abierto(self):
        if self.f_pais_a and self.f_pais_b:
            return True
        else:
            return False

    @abierto.setter
    def abierto(self, bool):
        if type(bool) is type(True):
            self.f_pais_b = bool
            self.f_pais_a = bool
        else:
            raise ValueError

    def __eq__(self, other):
        if self.pais_a == other.pais_a and self.pais_b == other.pais_b:
            return True
        elif self.pais_b == other.pais_a and self.pais_a == other.pais_b:
            return True
        else:
            return False

    def __repr__(self):
        if self.abierto:
            conexion = "<->"
        else:
            conexion = "| / |"
        return "{} {} {}".format(self.pais_a, conexion, self.pais_b)

    def cerrar(self):
        self.abierto = False

    def abrir(self):
        self.abierto = True
