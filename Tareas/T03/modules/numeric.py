def __columna(dato: any, *args) -> bool:
    """
    
    :param dato: any
    :return: boolean
    """
    return not any(("__iter__" in dir(dato), "__getitem__" in dir(dato) and "__len__" in dir(dato)))


def prom(datos: any, *args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """
    if __columna(datos):
        # Lanzar error de datos
        pass
    return float(sum(datos)/len(datos))


def desv(datos: any,*args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """
    return float(sum([(datos[i]-prom(datos))**2for i in range(0, len(datos))])/(len(datos)-1))**(1/2)


def median(datos: any,*args) -> any:
    """
    
    :param datos: Columna
    :return: int or float
    """
    return (prom((datos[len(datos)//2-1],datos[len(datos)//2])) if len(datos)%2 == 0 else datos[len(datos)//2])


def var(datos: any, *args) -> float:
    """
    
    :param datos: Columna
    :return: float
    """
    return desv(datos) ** 2


numeric = {"LEN": len, "PROM": prom, "DESV": desv, "MEDIAN": median, "VAR": var}

if __name__ == "__main__":
    datos = [1, 2, 3, 4, 5, 6, 7, 8, 8]
    print(datos)
    [print(numeric[funcion](datos)) for funcion in numeric.keys()]
