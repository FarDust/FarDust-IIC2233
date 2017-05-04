from modules.boolean import boolean
from modules.numeric import numeric
from modules.distro import crear_funcion
from errors import InvalidCommand,InvalidArgument
from itertools import tee


def asign(variable: str, comando: any) -> None:
    """
    
    :param variable: str 
    :param comando: any
    :return: None
    """
    if type(variable) != str:
        raise TypeError("asignar({} <- ,{})".format(variable, comando))
    if variable in keys:
        raise InvalidCommand("asignar({} <- ,{})".format(variable, comando))
    asignar[variable] = comando
    if __name__ == "__main__":
        print("se asigno {} a {}".format(comando, variable))


def graficar(columna: any, opcion: any) -> None:
    """
    
    :param columna: Columna 
    :param opcion: str or Columna
    :return: None
    """
    import matplotlib.pyplot as plt
    columna = tee(iter(columna))
    if opcion in ("numerico", "normalizado"):
        if opcion == "numerico":
            plt.plot(*zip(*enumerate(columna[0])), 'k-', linewidth=2)
        else:
            total = sum(columna[1])
            plt.plot(*zip(*((tupla[0] / total, tupla[1]) for tupla in (enumerate(columna[0])))), 'k-', linewidth=2)
    if opcion.find("rango:") != -1:
        try:
            (a, b, c) = tuple((int(i) if i.isdigit() else float(i)) for i in opcion[opcion.find("rango:") + 6:].split(","))
        except ValueError:
            raise TypeError("")
        if (a < b and c < 0) or (a > b and c > 0):
            raise InvalidArgument
        print(sorted(list(a+i*c for i in range(abs(int((b-a)/c))))))
        plt.plot(list(a+i*c for i in range(int((a-b)/c))),list(columna[0]), 'k-', linewidth=2)


    plt.show()
    pass


keys = {}
basics = {"asignar": asign, "crear_funcion": crear_funcion, "graficar": graficar}
asignar = {}
functions = {}

[keys.update(dic) for dic in (basics, boolean, numeric)]
keys = keys.keys()

if __name__ == "__main__":
    graficar([10, 12, 13], "rango:60,20,-0.1")
