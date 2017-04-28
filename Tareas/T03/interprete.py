from modules.numeric import numeric
from modules.boolean import boolean
from modules.basic import basics, asignar
from typing import *

comandos = {}
comandos.update(numeric)
comandos.update(boolean)


def interpretar(consulta: Iterable) -> any:
    if __name__ == "__main__":
        print("-----------------------------------")
        print("Entrando a la consulta: ",consulta)
    if "__getitem__" in dir(consulta) and "__len__" in dir(consulta) and type(consulta) != str:
        try:
            consulta = list(consulta)
        except:
            raise TypeError("Error de tipo")
    if "__len__" in dir(consulta) and len(consulta) == 0 and type(consulta) != str:
        return consulta
    elif consulta in asignar.keys():
        return asignar[consulta[0]]
    elif consulta[0] in comandos.keys():
        return comandos[consulta[0]](*[interpretar(nodo) for nodo in consulta[1:]])
    elif len(list(filter(lambda x: type(x) is int or type(x) is float, consulta))) == 0:
        return consulta
    if __name__ == "__main__":
        print("-----------------------------------")


if __name__ == "__main__":
    #print(comandos.keys())
    #print("Consulta 1:")
    #print(interpretar(["LEN",[1, 2, 3]]))
    #interpretar({"2": 2})
    print("Consulta 2:")
    print(interpretar(["comparar", ["PROM", "x"], ">", ["DESV", "y"]]))
    #consulta = 2
    #try:
    #    interpretar(consulta)
    #except TypeError:
    #    print("Error de consulta:", consulta)
    #    print("Causa: Error de tipo")
