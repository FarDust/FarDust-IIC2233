# Empieza la fiesta
from leemundo import generar_aeropuertos, generar_fronteras, generar_paises
from mundo import Mundo
from infeccciones import Virus, Bacteria, Parasito
from super_lista import Lista


def iniciar():
    resp = None
    print("1. Nuevo")
    print("2. Cargar")
    while resp not in Lista("1", "2"):
        resp = input("Respuesta: ")
        if resp == "2":
            return cargar()
    infeccion = None
    inicial = None
    paises = generar_paises()
    while not infeccion or not inicial:
        print("1. Seleccionar infeccion")
        print("2. Seleccionar pais")
        respuesta = input("Respuesta: ")
        if respuesta == "1":
            print("Infecciones")
            print("1. Virus")
            print("2. Bacteria")
            print("3. Parasito")
            ans = input("Respuesta: ")
            if ans == "1":
                infeccion = Virus()
            elif ans == "2":
                infeccion = Bacteria()
            elif ans == "3":
                infeccion = Parasito()
        elif respuesta == "2":
            for pais in paises:
                print(pais.nombre)
            res = input("Escriba el pais donde comenzar: ").lower().title()
            try:
                inicial = Lista(*filter(lambda pais: pais.nombre == res, paises))[0]
            except:
                print("El pais no existe")
    planeta = Mundo(generar_aeropuertos(generar_fronteras(paises)), infeccion)
    inicial.poblacion.infectar()
    planeta.actualizar()
    return planeta


def menu():
    print("1. Pasar dia")
    print("2. Estadisticas")
    print("3. Guardar")
    print("x. Salir")
    respuesta = input("Respuesta: ").lower()
    if respuesta == "1":
        pasar_dia()
    elif respuesta == "2":
        estadisticas()
    elif respuesta == "3":
        guardar()
    elif respuesta == "x":
        salir()


def cargar():
    try:
        open("save.txt", "r")
    except:
        print("No hay partida anterior")
        return iniciar()


def pasar_dia():
    planeta.actualizar()
    print("{}".format(planeta).center(100))
    print("{}{}".format("-" * int(planeta.per_muertos), "+" * int(planeta.per_infeccion)).ljust(100, "="))


def guardar():
    pass


def estadisticas():
    salir = False
    while not salir:
        print("Estadisticas")
        print("1. Por pais\n2. Mundo\n3. Tasas\n4. Sucesos\nx. salir")
        respuesta = input("Respuesta: ")
        if respuesta == "x":
            salir = True
        elif respuesta == "1":
            pais = input("Ingrese un pais: ").lower().title()
            try:
                planeta.resumen_pais(pais)
            except:
                print("Pais no existe")
        elif respuesta == "2":
            planeta.resumen_global()
        elif respuesta == "3":
            planeta.muertes_infecciones()
        elif respuesta == "4":
            # Resumen del dia
            leer_sucesos()
        elif respuesta == "x":
            salir = True


def leer_sucesos():
    print(open("sucesos.txt", "r").read())

def salir():
    raise SystemExit


if __name__ == "__main__":
    planeta = iniciar()
    while True:
        menu()
        if planeta.poblacion_infectada == 0 and planeta.poblacion_muerta == planeta.poblacion_mundial:
            print("Ganaste")
            print("Transcurrieron {} dias hasta el final".format(planeta.dias))
            raise SystemExit
        elif planeta.poblacion_infectada == 0:
            print("Perdiste")
            print("Transcurrieron {} dias hasta el final".format(planeta.dias))
            raise SystemExit
