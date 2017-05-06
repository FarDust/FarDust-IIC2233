from errors import InvalidCommand, InvalidArgument
from itertools import tee


def extraer_columna(nombre_archivo: str, head: str, *args) -> any:
    """
    
    :param nombre_archivo: str
    :param head: str
    :return: Columna
    """
    if len(args) > 0:
        raise InvalidArgument
    if not (type(nombre_archivo) is str):
        raise TypeError("extraer_columna({} <-,{})".format(nombre_archivo, head))
    elif not (type(head) is str):
        raise TypeError("extraer_columna({},{} <-)".format(nombre_archivo, head))
    elif "." in nombre_archivo:
        raise InvalidCommand("extraer_columna({} <-,{})".format(nombre_archivo, head))
    try:
        if __name__ == "__main__":
            nombre_archivo = "../" + nombre_archivo
        archivo = (open(nombre_archivo + ".csv", "r", encoding="UTF8"))
        n = tuple(
            (valor.split(":")[1] if valor.split(":")[0] == head else None) for valor in
            (next(archivo)).strip().split(";"))
        (numero, tipo) = next(
            filter(lambda x: x[1] is not None, (((i, n[i]) if i is not None else None) for i in range(len(n)))))
        if numero == -1 or numero is None:
            raise InvalidCommand
        raw = (linea.strip().split(";")[numero] for linea in archivo)
        return (_aplicar_tipo(valor, tipo) for valor in raw)
    except FileNotFoundError:
        raise InvalidCommand


def _aplicar_tipo(valor: str, tipo: str) -> any:
    if tipo == "int":
        return int(valor)
    elif tipo == "float":
        return float(valor)
    else:
        raise TypeError


def filtrar(columna: any, simbolo: str, valor: any, *args) -> any:
    """
    
    :param columna: Columna
    :param simbolo: str
    :param valor: int or float
    :return: Columna
    """
    if not (type(valor) is int or type(valor) is float):
        raise TypeError
    if type(columna) is str:
        raise TypeError
    if type(columna) is list:
        columna = iter(columna)
    if not "__iter__" in dir(columna):
        raise TypeError
    if simbolo == "<":
        return filter(lambda x: x < valor, columna)
    elif simbolo == ">":
        return filter(lambda x: x > valor, columna)
    elif simbolo == ">=":
        return filter(lambda x: x >= valor, columna)
    elif simbolo == "<=":
        return filter(lambda x: x <= valor, columna)
    elif simbolo == "==":
        return filter(lambda x: x == valor, columna)
    elif simbolo == "!=":
        return filter(lambda x: x != valor, columna)
    else:
        raise InvalidCommand


def operar(columna: any, simbolo: str, valor: any, *args) -> any:
    """
    
    :param columna: Columna
    :param simbolo: str
    :param valor: int or float
    :return: Columna
    """
    if len(args) > 0:
        raise InvalidArgument
    operadores = {"+", "-", "*", "/", ">=<"}
    try:
        columna = tee(iter(columna))
    except TypeError:
        raise TypeError("operar({} <-,{},{})".format("columna", simbolo, valor))
    if type(columna) is str:
        raise TypeError("operar({} <-,{},{})".format("columna", simbolo, valor))
    if not type(valor) is int or not type(valor) is float:
        raise TypeError("operar({},{},{} <-)".format("columna", simbolo, valor))
    if simbolo in operadores:
        if simbolo == "+":
            return (i + valor for i in columna)
        elif simbolo == "-":
            return (i - valor for i in columna)
        elif simbolo == "*":
            return (i * valor for i in columna)
        elif simbolo == "/":
            if valor != 0:
                return (i / valor for i in columna)
            raise ZeroDivisionError
        else:
            if int(valor) > 0:
                return (round(i, int(valor)) for i in columna)
            else:
                raise TypeError
    else:
        raise TypeError("operar({},{} <-,{})".format("columna", simbolo, valor))


def evaluar(funcion: any, inicio: any, final: any, intervalo: any, *args) -> any:
    """
    
    :param funcion: funcion
    :param inicio: int or float
    :param final: int or float
    :param intervalo: int or float
    :return: Columna
    """
    if intervalo == 0:
        raise ZeroDivisionError
    if len(args) > 0:
        raise InvalidArgument
    if not "__call__" in dir(funcion):
        raise InvalidCommand
    if "__call__" not in dir(funcion):
        raise TypeError
    if not (type(inicio) is int or type(inicio) is float):
        raise TypeError
    elif not (type(final) is int or type(final) is float):
        raise TypeError
    elif not (type(intervalo) is int or type(intervalo) is float):
        raise TypeError
    return map(lambda x: funcion(x), (inicio + i * intervalo for i in range(int((final - inicio) / intervalo))))


datos = {"extraer_columna": extraer_columna, "filtrar": filtrar, "operar": operar, "evaluar": evaluar}

if __name__ == "__main__":
    # [print(i) for i in (extraer_columna("registros", "tiempo_infectado"))]

    operar(1523, "+", 2)


    def func(x):
        return x ** 2


    print(list(evaluar(func, -3, 5.1, 0.2)))
