from modules.boolean import boolean
from modules.numeric import numeric
from modules.distro import crear_funcion
from errors import InvalidCommand


def asign(variable: str, comando: any) -> None:
    """
    
    :param variable: str 
    :param comando: any
    :return: None
    """
    if type(variable) != str:
        raise TypeError("asignar({} <- ,{})".format(variable, comando))
    if variable in keys:
        raise InvalidCommand("asignar({} <- ,{})".format(variable, comando))
    asignar[variable] = comando
    if __name__ == "__main__":
        print("se asigno {} a {}".format(comando, variable))


def graficar(columna: any, opcion: any) -> None:
    """
    
    :param columna: Columna 
    :param opcion: str or Columna
    :return: None
    """
    pass


keys = {}
basics = {"asignar": asign, "crear_funcion": crear_funcion, "graficar": graficar}
asignar = {}
functions = {}

[keys.update(dic) for dic in (basics, boolean, numeric)]
keys = keys.keys()

if __name__ == "__main__":
    print(keys)
