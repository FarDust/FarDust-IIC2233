from errors import InvalidArgument


def comparar_columna(columna_1: any, simbolo: str, comando: str, columna_2: any, *args) -> any:
    """
    
    :param columna_1: Columna
    :param simbolo: str
    :param comando: str ("LEN","PROM","DESV","MEDIAN","VAR")
    :param columna_2: Columna
    :return: any 
    """
    if len(args) > 0:
        raise InvalidArgument
    from itertools import tee
    columna_1 = iter(columna_1)
    columna_2 = iter(columna_2)
    gen = (*tee(columna_1), *tee(columna_2))
    columna_1 = gen[0]
    columna_2 = gen[2]
    from modules.numeric import numeric
    if comando not in numeric.keys():
        raise TypeError
    try:
        if len(list(filter(lambda x: not (type(x) == float or type(x) == int), [i for i in gen[1]]))) != 0:
            raise TypeError
        elif len(list(filter(lambda x: not (type(x) == float or type(x) == int), [i for i in gen[3]]))) != 0:
            raise TypeError
    except IndexError:
        raise TypeError
    if simbolo == "<":
        return numeric[comando](columna_1) < numeric[comando](columna_2)
    elif simbolo == ">":
        return numeric[comando](columna_1) > numeric[comando](columna_2)
    elif simbolo == ">=":
        return numeric[comando](columna_1) >= numeric[comando](columna_2)
    elif simbolo == "<=":
        return numeric[comando](columna_1) <= numeric[comando](columna_2)
    elif simbolo == "==":
        return numeric[comando](columna_1) == numeric[comando](columna_2)
    elif simbolo == "!=":
        return numeric[comando](columna_1) != numeric[comando](columna_2)
    else:
        raise TypeError


def comparar(numero_1: any, simbolo: str, numero_2: any, *args) -> any:
    """
    
    :param numero_1: int or float
    :param simbolo: str
    :param numero_2: int or float
    :return: any
    """
    if len(args) > 0:
        raise InvalidArgument
    if simbolo == "<":
        return numero_1 < numero_2
    elif simbolo == ">":
        return numero_1 > numero_2
    elif simbolo == ">=":
        return numero_1 >= numero_2
    elif simbolo == "<=":
        return numero_1 <= numero_2
    elif simbolo == "==":
        return numero_1 == numero_2
    elif simbolo == "!=":
        return numero_1 != numero_2
    else:
        raise TypeError


boolean = {"comparar": comparar, "comparar_columna": comparar_columna}

if __name__ == "__main__":
    simbolos = {">", "<", "<=", ">=", "==", "!="}
    [print(comparar_columna([1, 2, 3, 4, 5], simbolo, "MEDIAN", [1, 2, 5, 5, 5])) for simbolo in simbolos]
    print("")
    [print(comparar(5, simbolo, 7.0)) for simbolo in simbolos]
