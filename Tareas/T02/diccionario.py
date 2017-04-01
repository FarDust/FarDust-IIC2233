from super_lista import Lista


class Posicionado:
    def __init__(self, *args):
        args = Lista(*args)
        if len(args) %2 != 0:
            raise ValueError
        self.__llaves = Lista()
        self.__valores = Lista()
        for i in range(len(args)):
            if i%2 !=0:
                self.__valores.append(args[i])
            else:
                self.__llaves.append(args[i])

    def items(self):
        return Lista(self.__llaves, self.__valores)

    def values(self):
        return self.__valores

    def keys(self):
        return self.__llaves

    def append(self, valor1, valor2):
        if valor1 in self.__llaves:
            i = self.__llaves.index(valor1)
            self.__valores.pop(i)
            self.__valores.append(valor2)
        else:
            self.__llaves.append(valor1)
            self.__valores.append(valor2)

    def pop(self, i=None):
        a = self.__llaves.pop(i)
        b = self.__valores.pop(i)
        return Lista(a,b)

    def __len__(self):
        return len(self.__llaves)

    def __index__(self,key):
        pass

    def __getitem__(self, key):
        return self.__valores[self.__llaves.index(key)]

    def __repr__(self):
        string = "/"
        for items in range(len(self)):
            string += "{} -> {}".format(self.items()[0][items], self.items()[1][items])
            if items < len(self)-1:
                string += ","
        string += "/"
        return string

