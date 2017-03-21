# Dibujar v1.0.0
from os import system


def borrar():
    try:
        system("cls")
    except:
        try:
            system("clear")
        except:
            print("------------------------------")

def frame(mensaje=""):
    borrar()
    print(mensaje)
