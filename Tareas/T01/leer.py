# leer v1.0.0

from abc import ABCMeta, abstractproperty


class Leer(metaclass=ABCMeta):
    def __init__(self, archivo):
        self.archivo = archivo
        pass

    @abstractproperty
    def Diccionario(self):
        pass

    @staticmethod
    def Tipo(tipo, value):
        if tipo == "string":
            return str(value)
        else:
            # tratar de obtener el tipo mediante string sin romperse la cabeza
            return


class Users(Leer):
    def __init__(self, archivo):
        super().__init__(archivo)

    @property
    def Diccionario(self):
        with open(self.archivo, "r", encoding="utf8") as lectura:
            temp = lectura.readline().strip().split(",")
            dic = {}
            for i in temp:
                dic[(str(i[:i.find(":")]))] = i[i.find(":") + 1:]
            temp.clear()
            lectura.close()
        return dic

    def completar(self, id):
        id = str(id)
        with open(self.archivo, "r", encoding="utf8") as lectura:
            base = lectura.read()
            temp = base[base.find("\n" + id):base.find("\n" + str(int(id) + 1))].strip().split(",")
            dic = {}
            n = 0
            for key, valor in self.Diccionario.items():
                dic[key] = self.Tipo(valor, temp[n])
                n += 1
            temp.clear()
            lectura.close()
        return dic

# a = Users("usuarios.csv")
# print(a.Diccionario)
# print(a.completar(9))
