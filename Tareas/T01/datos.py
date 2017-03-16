class BaseDeDatos:
    def __init__(self):
        pass

    def leer_usuarios(self):
        usuarios = open("usuarios.csv", "r+")
        print(usuarios.read())
        usuarios.close()


usuarios = open("usuarios.csv", "r")
print(usuarios.read())
usuarios.close()
