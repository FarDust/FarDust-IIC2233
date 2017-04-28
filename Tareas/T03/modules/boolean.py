def comparar_columna(columna_1: any, simbolo: str, comando: str, columna_2: any) -> any:
    """
    
    :param columna_1: Columna
    :param simbolo: str
    :param comando: str ("LEN","PROM","DESV","MEDIAN","VAR")
    :param columna_2: Columna
    :return: any 
    """
    from modules.numeric import numeric
    if comando not in numeric.keys():
        raise TypeError("Error de tipo")
    try:
        if len(list(filter(lambda x: not (type(x) == float or type(x) == int), [i for i in columna_1]))) != 0:
            raise TypeError("Error de tipo")
        elif len(list(filter(lambda x: not (type(x) == float or type(x) == int), [i for i in columna_2]))) != 0:
            raise TypeError("Error de tipo")
    except IndexError:
        raise TypeError("Error de tipo")
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
        raise TypeError("Error de tipo")


def comparar(numero_1: any, simbolo: str, numero_2: any) -> any:
    """
    
    :param numero_1: int or float
    :param simbolo: str
    :param numero_2: int or float
    :return: any
    """
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
        raise TypeError("Error de tipo")

boolean = {"comparar": comparar, "comparar_columna": comparar_columna}

if __name__ == "__main__":
    simbolos = {">", "<", "<=", ">=", "==", "!="}
    [print(comparar_columna([1, 2, 3, 4, 5], simbolo, "MEDIAN", [1, 2, 5, 5, 5])) for simbolo in simbolos]
    print("")
    [print(comparar(5, simbolo, 7.0)) for simbolo in simbolos]