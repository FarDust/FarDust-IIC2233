from errors import InvalidArgument
from itertools import tee


def arguments(funcion):
    def _arguments(datos, *args):
        if len(args) != 0:
            raise InvalidArgument
        return funcion(datos)

    return _arguments


@arguments
def prom(datos: any, *args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """
    if "__iter__" in dir(datos):
        gen = tee(datos)
        (datos, land) = (gen[0], long(gen[1]))
    else:
        land = long(datos)
    if land == 0:
        raise ZeroDivisionError
    return float(sum(datos) / land)


@arguments
def desv(datos: any, *args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """
    if type(datos) is list:
        datos = iter(datos)
    if "__iter__" in dir(datos):
        gen = tee(datos)
        (datos, land) = (gen[0], long(gen[1]))
    else:
        land = long(datos)
    datos = tee(datos)
    promedium = prom(datos[1])
    if (land - 1) == 0:
        raise ZeroDivisionError
    return float(sum([(next(datos[0]) - promedium) ** 2 for i in range(0, land)]) / (land - 1)) ** (1 / 2)


@arguments
def median(datos: any, *args) -> any:
    """
    
    :param datos: Columna
    :return: int or float
    """
    if "__iter__" in dir(datos):
        gen = tee(datos)
        (datos, land) = (gen[0], long(gen[1]))
    else:
        land = long(datos)
    if land == 0:
        return None
    datos = list(datos)
    respuesta = prom((datos[land // 2 - 1], datos[land // 2])) if land % 2 == 0 else datos[land // 2]
    datos.clear()
    return respuesta


@arguments
def var(datos: any, *args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """

    return desv(datos) ** 2


@arguments
def long(datos: any):
    return len(list(datos))


numeric = {"LEN": long, "PROM": prom, "DESV": desv, "MEDIAN": median, "VAR": var}

if __name__ == "__main__":
    datos = [1, 2, 3, 4, 5, 6, 7, 8, 8]
    print(datos)
    [print(numeric[funcion](datos)) for funcion in numeric.keys()]
