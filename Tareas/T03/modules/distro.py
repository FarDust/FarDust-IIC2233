from errors import InvalidArgument
from math import e, pi
from sys import setrecursionlimit
setrecursionlimit(999)


def crear_funcion(*args):
    save = args
    args = iter(args)
    tipo = next(args)
    if tipo in {"normal", "exponencial", "gamma"}:
        if tipo == "normal":
            respuesta = normal(next(args), next(args))
        elif tipo == "exponencial":
            respuesta = exponencial(next(args))
        else:
            respuesta = gamma(next(args), next(args))
        if len(list(args)) > 0:
            raise InvalidArgument("crear_funcion({})".format(save))
        return respuesta
    else:
        raise TypeError


def normal(u, o):
    if o <= 0:
        raise InvalidArgument
    def normalizado(x):
        return (1 / (2 * pi * o ** 2) ** (1 / 2)) * e ** ((-1 / 2) * ((x - u) / o) ** 2)

    return normalizado


def exponencial(v):
    if v <= 0:
        raise InvalidArgument

    def exponential(x):
        if x < 0:
            raise InvalidArgument
        return v * e ** (-v * x)

    return exponential


def gamma(v,k):
    def gam(x):
        if x < 0:
            raise InvalidArgument
        return ((v ** k) / factorial(k - 1)) * (x ** (k - 1)) * e ** (-v * x)

    return gam


def factorial(x):
    if x <= 0:
        return 1

    return x * factorial(x - 1)


if __name__ == "__main__":
    print(factorial(5))
    a = crear_funcion("normal", 2, 3)
    print(a(5))
