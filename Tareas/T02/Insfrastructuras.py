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
    # Al crearse este objeto se guardara en los dos paises vecionos a la vez
    def __init__(self, *args):
        super().__init__()
        args = Lista(*args)
        self.pais_a = args[0]
        self.pais_b = args[1]
        self.statics_a = 0
        self.statics_b = 0
        self.f_pais_a = True
        self.f_pais_b = True

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


class RutaDeVuelo:
    def __init__(self, *args):
        args = Lista(*args)
        self.pais_a = args[0]
        self.pais_b = args[1]
        self.statics_a = None
        self.statics_b = None
        self.f_pais_a = True
        self.f_pais_b = True
        self.abierto = True
        self.infectada = False

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