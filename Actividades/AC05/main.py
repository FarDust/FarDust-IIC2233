
class CustomException(Exception):
    def __init__(self, letra,pos):
        super().__init__('A partir de esta letra: {} \nEl mensaje esta invertido\n'.format(letra))
        self.pos = pos


class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            try:
                for caracter in texto:
                    if "a" is caracter:
                        raise CustomException(caracter, texto.find("a"))
                    self.codigo += caracter
            except CustomException as err:
                print(err)
                temp = []
                for binario in texto[err.pos + 1:].split(" "):
                    temp.append(binario[::-1])
                texto2 = " ".join(temp)
                temp.clear()
                for caracter in texto2:
                    if "a" is caracter:
                        raise CustomException(caracter, texto.find("a"))
                    self.codigo += caracter
            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            if len(i) < 6 or len(i) > 7:
                pass
            else:
                self.codigo+=' '+i
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        while i < len(lista):
            i += 1
            try:
                if '$' != lista[i]:
                    string += lista[i]
            except IndexError as err:
                print("El golpe fue fuerte se detecto el siguiente error: {}".format(err))
        return string


if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        codigo= des.lectura_archivo()
        codigo=des.elimina_incorrectos()
        lista = des.cambiar_binarios(des.codigo)
        texto = des.limpiador(lista)
        print(texto)
    except AttributeError as err:
        print("{}: Se previnio una 's' faltante".format(err))
        des = Descifrador('mensaje_marciano.txt')
        codigo = des.lectura_archivo()
        codigo = des.elimina_incorrectos()
        lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
        print(texto)

    except Exception as err:
        print('Esto no debiese imprimirse')