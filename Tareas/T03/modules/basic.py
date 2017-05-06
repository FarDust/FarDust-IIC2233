from modules.boolean import boolean
from modules.numeric import numeric
from modules.distro import crear_funcion
from errors import InvalidCommand, InvalidArgument, InvalidRef
from itertools import tee


def asign(variable: str, comando: any, *args) -> str:
    """
    
    :param variable: str 
    :param comando: any
    :return: str("asignar")
    """
    if len(args) > 0:
        raise InvalidArgument
    if type(variable) != str:
        raise TypeError("asignar({} <- ,{})".format(variable, comando))
    if variable in keys:
        raise InvalidCommand("asignar({} <- ,{})".format(variable, comando))
    asignar[variable] = comando
    if __name__ == "__main__":
        print("se asigno {} a {}".format(comando, variable))
    return "asignar"


def graficar(columna: any, opcion: any, graph=False) -> str:
    """
    
    :param graph: 
    :param columna: Columna 
    :param opcion: str or Columna
    :return: str(graficar)
    """
    import matplotlib.pyplot as plt
    if type(columna) == str:
        raise InvalidRef
    columna = tee(iter(columna))
    if opcion in ("numerico", "normalizado"):
        if opcion == "numerico":
            plt.plot(*zip(*enumerate(columna[0])), 'k-', linewidth=2)
        else:
            total = sum(columna[1])
            plt.plot(*zip(*((tupla[0] / total, tupla[1]) for tupla in (enumerate(columna[0])))), 'k-', linewidth=2)
    elif type(opcion) == str and opcion.find("rango:") != -1:
        try:
            (a, b, c) = tuple(
                (int(i) if i.isdigit() else float(i)) for i in opcion[opcion.find("rango:") + 6:].split(","))
        except ValueError:
            raise TypeError
        if (a < b and c < 0) or (a > b and c > 0):
            raise InvalidArgument
        # print(len(sorted(list(a + i * c for i in range(int(abs(a - b) / c)))[:len(list(columna[1]))])))
        # print(len(list(columna[0])))
        plt.plot(sorted(list(a + i * c for i in range(int(abs(a - b) / c)))[:len(list(columna[1]))]), list(columna[0]),
                 'k-', linewidth=2)
    elif type(opcion) == str:
        raise TypeError
    else:
        columna2 = tee(iter(opcion))
        if len(list(columna2[0])) == len(list(columna[0])):
            plt.plot(list(columna2[1]), list(columna[1]), 'k-', linewidth=2)
    if graph is True:
        plt.show()
    return "graficar"
    pass


keys = {}
basics = {"asignar": asign, "crear_funcion": crear_funcion, "graficar": graficar}
asignar = {}
functions = {}

[keys.update(dic) for dic in (basics, boolean, numeric)]
keys = keys.keys()

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    graficar([10, 12, 13], "rango:-3,5,0.1")

    plt.show()
