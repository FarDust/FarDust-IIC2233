from modules.numeric import numeric
from modules.boolean import boolean
from modules.basic import basics, asignar
from modules.datos import datos
from itertools import tee
from errors import InvalidArgument, InvalidRef, InvalidCommand


def comprobar(interprete):
    def _interpretar(consulta, graph):
        return interprete(consulta, graph)

    return _interpretar


@comprobar
def interpretar(consulta, graph=False) -> any:
    if __name__ == "__main__":
        print("-----------------------------------")
        print("Entrando a la consulta: ", consulta, "|tipo:", type(consulta))
    if "__getitem__" in dir(consulta) and "__len__" in dir(consulta) and type(consulta) != str:
        respaldo = (str(i) for i in consulta)
        try:
            consulta = list(consulta)
        except:
            raise TypeError
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
        if __name__ == "__main__":
            print("consulta fantasma: {}".format(consulta))
            print(asignar.keys())
        return consulta
    elif type(consulta) is int or type(consulta) is float:
        return consulta
    elif not type(consulta[0]) is list and consulta[0] in comandos.keys():
        support = ",".join([str(i) for i in consulta[1:]])
        try:
            if consulta[0] == "asignar":
                return comandos[consulta[0]](consulta[1], *[interpretar(nodo, graph) for nodo in consulta[2:]])
            elif consulta[0] == "do_if":
                return comandos[consulta[0]](*consulta[1:], graph)
            else:
                if graph is True and consulta[0] == "graficar":
                    res = comandos[consulta[0]](*[interpretar(nodo, graph) for nodo in consulta[1:]], graph=graph)
                    return res
                return comandos[consulta[0]](*[interpretar(nodo, graph) for nodo in consulta[1:]])
        except TypeError:
            return "Consulta :{}({})\nCausa: Error de tipo".format(str(consulta[0]), support)
        except ZeroDivisionError:
            return "Consulta :{}({})\nCausa: Error matematico".format(str(consulta[0]), support)
        except InvalidArgument:
            return "Consulta :{}({})\nCausa: Argumento invalido".format(str(consulta[0]), support)
        except InvalidRef:
            return "Consulta :{}({})\nCausa: Referencia invalida".format(str(consulta[0]), support)
        except InvalidCommand:
            return "Consulta :{}({})\nCausa: Imposible procesar".format(str(consulta[0]), support)
        except Exception as err:
            return err
    elif len(list(filter(lambda x: not (type(x) is int or type(x) is float), consulta))) == 0:
        return consulta
    elif type(consulta) is list:
        respuesta = tuple(
            str(i[1]) + "\n" + str(i[0]) for i in
            zip(tuple(interpretar(nodo, graph) for nodo in consulta), tuple(respaldo)))
        return respuesta
    else:
        return consulta


def do_if(consulta_a, consulta_b, consulta_c, graph) -> any:
    consult = interpretar(consulta_b, graph)
    if not type(consult) is bool:
        raise InvalidArgument
    if consult is True:
        return interpretar(consulta_a, graph)
    else:
        return interpretar(consulta_c, graph)


comandos = {"do_if": do_if}
comandos.update(numeric)
comandos.update(boolean)
comandos.update(basics)
comandos.update(datos)

if __name__ == "__main__":
    # print("Superconsulta:")
    # a = interpretar([['asignar', 'x', ['extraer_columna', 'registros', 'tiempo_sano']],
    #                  ['asignar', 'y', ['extraer_columna', 'registros', 'muertos_avistados']],
    #                  ['comparar', ['PROM', 'x'], '>', ['DESV', 'y']],
    #                  ['asignar', 'filtrado', ['filtrar', 'x', '>', 100]],
    #                  ['asignar', 'funcion_normal', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]],
    #                  ['PROM', 'filtrado'], ['VAR', 'funcion_normal'],
    #                  ['do_if', ['VAR', 'funcion_normal'], ['comparar_columna', 'funcion_normal', '>', 'DESV', 'x'],
    #                   ['PROM', 'x']]], True)
    # b = interpretar([['asignar', 'funcion_normal', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]],
    #                  ['graficar', 'funcion_normal', 'rango: -3,5,0.1']], True)
    c = interpretar([['asignar', 'x', ['extraer_columna', 'registros', 'tiempo_sano']],
                     ['asignar', 'y', ['extraer_columna', 'registros', 'muertos_avistados']],
                     ['comparar', ['PROM', 'x'], '>', ['DESV', 'y']],
                     ['asignar', 'filtrado', ['filtrar', 'x', '>', 100]],
                     ['asignar', 'funcion_normal', ['evaluar', ['crear_funcion', 'normal', 0, 0.5], -3, 5, 0.1]],
                     ['PROM', 'filtrado'], ['VAR', 'funcion_normal'],
                     ['do_if', ['VAR', 'funcion_normal'], ['comparar_columna', 'funcion_normal', '>', 'DESV', 'x'],
                      ['PROM', 'x']], ['graficar', 'filtrado', 'numerico'], ['graficar', 'normal', 'rango: -3,5,0.1'],
                     ['asignar', 'gamma',
                      ['evaluar', ['crear_funcion', 'gamma', 2, 0.16666666666666666], 0, 40, 4e-05]],
                     ['comparar_columna', 'x', '>', 'DESV', 'gamma'], ['graficar', 'x', 'rango: 0.00004, 40, 0.00004'],
                     ['graficar', 'x', 'normalizado']], False)
    print(asignar.values())
    [print(i + "\n") for i in c]
