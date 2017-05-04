from modules.numeric import numeric
from modules.boolean import boolean
from modules.basic import basics, asignar
from modules.datos import datos
from itertools import tee
from errors import InvalidArgument
from typing import *

def interpretar(consulta: Iterable) -> any:
    if __name__ == "__main__":
        print("-----------------------------------")
        print("Entrando a la consulta: ", consulta, "|tipo:", type(consulta))
    if "__getitem__" in dir(consulta) and "__len__" in dir(consulta) and type(consulta) != str:
        try:
            consulta = list(consulta)
        except:
            raise TypeError("Error de tipo")
    generator = (i for i in range(1))
    if type(consulta) != str and "__len__" in dir(consulta) and len(consulta) == 0:
        return consulta
    elif type(consulta) is type(generator):
        return tee(consulta)[1]
    elif type(consulta) is str and consulta in asignar.keys():
        if "__iter__" in dir(asignar[consulta]):
            gen = tee(asignar[consulta])
            asignar[consulta] = gen[0]
            return gen[1]
        return asignar[consulta]
    elif type(consulta) is str:
        # if __name__ == "__main__":
        #     print("consulta fantasma: {}".format(consulta))
        #     print(asignar.keys())
        print("consulta fantasma: {}".format(consulta))
        print(asignar.keys())
        return consulta
    elif type(consulta) is int or type(consulta) is float:
        return consulta
    elif not type(consulta[0]) is list and consulta[0] is "do_if":
        return comandos[consulta[0]](*consulta[1:])
    elif not type(consulta[0]) is list and consulta[0] in comandos.keys():
        return comandos[consulta[0]](*[interpretar(nodo) for nodo in consulta[1:]])
    elif len(list(filter(lambda x: not (type(x) is int or type(x) is float), consulta))) == 0:
        return consulta
    elif type(consulta) is list:
        respuesta = tuple(interpretar(nodo) for nodo in consulta)
        if len(respuesta) == 1:
            return respuesta[0]
        return respuesta
    else:
        return consulta


def do_if(consulta_a, consulta_b, consulta_c) -> any:
    consulta_b = interpretar(consulta_b)
    if not type(consulta_b) is bool:
        raise TypeError("")
    if consulta_b is True:
        return interpretar(consulta_a)
    else:
        return interpretar(consulta_c)

comandos = {"do_if": do_if}
comandos.update(numeric)
comandos.update(boolean)
comandos.update(basics)
comandos.update(datos)

if __name__ == "__main__":
    # print("Consulta 1:")
    # print(interpretar([["LEN", [1, 2, 3]]]))
    # print("Consulta 2:")
    # print(interpretar([['asignar', 'x', ['extraer_columna', 'registros', 'tiempo_sano']]]))
    # print("Consulta 3:")
    # print(interpretar([['asignar', 'y', ['extraer_columna', 'registros', 'muertos_avistados']]]))
    # print("consulta 4:")
    # print(interpretar([["comparar", ["PROM", "x"], ">", ["DESV", "y"]]]))
    # print("consulta: 5")
    # print(interpretar([['asignar', 'funcion_normal', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]]]))
    # print("Consulta 6:")
    # print(interpretar([['do_if', ['VAR', 'funcion_normal'], ['comparar_columna', 'funcion_normal', '>', 'DESV', 'x'], ['PROM', 'x']]]))
    print("Superconsulta:")
    print(interpretar([['asignar', 'x', ['extraer_columna', 'registros', 'tiempo_sano']], ['asignar', 'y', ['extraer_columna', 'registros', 'muertos_avistados']], ['comparar', ['PROM', 'x'], '>', ['DESV', 'y']], ['asignar', 'filtrado', ['filtrar', 'x', '>', 100]], ['asignar', 'funcion_normal', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]], ['PROM', 'filtrado'], ['VAR', 'funcion_normal'], ['do_if', ['VAR', 'funcion_normal'], ['comparar_columna', 'funcion_normal', '>', 'DESV', 'x'], ['PROM', 'x']]]))

