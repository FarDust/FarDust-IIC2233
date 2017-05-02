from errors import InvalidCommand


def extraer_columna(nombre_archivo: str, head: str) -> any:
    """
    
    :param nombre_archivo: str
    :param head: str
    :return: Columna
    """
    if not (type(nombre_archivo) is str):
        raise TypeError("extraer_columna({} <-,{})".format(nombre_archivo, head))
    elif not (type(head) is str):
        raise TypeError("extraer_columna({},{} <-)".format(nombre_archivo, head))
    elif "." in nombre_archivo:
        raise InvalidCommand("extraer_columna({} <-,{})".format(nombre_archivo, head))
    if __name__ == "__main__":
        nombre_archivo = "../" + nombre_archivo
    archivo = (open(nombre_archivo + ".csv", "r", encoding="UTF8"))
    n = tuple(
        (valor.split(":")[1] if valor.split(":")[0] == head else None) for valor in (next(archivo)).strip().split(";"))
    (numero, tipo) = next(
        filter(lambda x: x[1] is not None, (((i, n[i]) if i is not None else None) for i in range(len(n)))))
    raw = (linea.strip().split(";")[numero] for linea in archivo)
    return (_aplicar_tipo(valor, tipo) for valor in raw)


def _aplicar_tipo(valor: str, tipo: str) -> any:
    if tipo == "int":
        return int(valor)
    elif tipo == "float":
        return float(valor)
    else:
        raise TypeError


def filtrar(columna: any, simbolo: str, valor: any) -> any:
    """
    
    :param columna: Columna
    :param simbolo: str
    :param valor: int or float
    :return: Columna
    """
    if type(columna) is list:
        columna = iter(columna)
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
        raise TypeError("Error de tipo")


def operar(columna: any, simbolo: str, valor: any) -> any:
    """
    
    :param columna: Columna
    :param simbolo: str
    :param valor: int or float
    :return: Columna
    """
    pass


def evaluar(funcion: any, inicio: any, final: any, intervalo: any) -> any:
    """
    
    :param funcion: funcion
    :param inicio: int or float
    :param final: int or float
    :param intervalo: int or float
    :return: Columna
    """
    inicio+ intervalo,inicio + 2*intervalo

    return map(lambda x: funcion(x), (inicio+i*intervalo for i in range(int((final - inicio)/intervalo))))
    pass


datos = {"extraer_columna": extraer_columna, "filtrar": filtrar, "operar": operar, "evaluar": evaluar}

if __name__ == "__main__":
    #[print(i) for i in (extraer_columna("registros", "tiempo_infectado"))]


    def func(x):
        return x ** 2


    print(list(evaluar(func, -3, 5.1, 0.2)))
