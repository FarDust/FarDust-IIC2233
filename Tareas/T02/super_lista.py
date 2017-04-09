class Nodo:
    # Estructura base de la lista
    def __init__(self, valor=None):
        # siguiente y anterior reciben nodos
        self.siguiente = None
        self.anterior = None
        # Valor resive un valor cualquiera
        self.valor = valor

    def __repr__(self):
        return str(self.valor)

    def __str__(self):
        return str(self.valor)


# Destaco que esto aunque lo llame lista no es una lista, como tal

class Lista:
    # Estructura basica de la lista, recibe nodos
    def __init__(self, *args):
        self.cola = None
        self.cabeza = None
        for i in args:
            self.append(i)

    def appendleft(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            nodo = Nodo(valor)
            nodo.siguiente = self.cabeza
            self.cabeza.anterior = nodo
            self.cabeza = self.cabeza.anterior

    @property
    def len(self):
        nodo = self.cabeza
        len = 0
        while nodo:
            nodo = nodo.siguiente
            len += 1
        return len

    def __len__(self):
        return self.len

    def append(self, valor):
        if not self.cabeza:
            self.cabeza = Nodo(valor)
            self.cola = self.cabeza
        else:
            nodo = Nodo(valor)
            nodo.anterior = self.cola
            self.cola.siguiente = nodo
            self.cola = self.cola.siguiente

    def find(self, pos):
        return self.__find_nodo(pos).valor

    def __find_nodo(self, pos):
        nodo = self.cabeza

        for i in range(pos):
            if nodo:
                nodo = nodo.siguiente
        if nodo:
            return nodo

    def index(self, valor):
        nodo = self.cabeza

        for i in range(self.len):
            if nodo and nodo.valor == valor:
                return i
            nodo = nodo.siguiente
        raise IndexError

    def __assit_getitem(self, pos):
        nodo = self.cabeza

        for i in range(pos):
            if nodo:
                nodo = nodo.siguiente
        if nodo:
            return nodo

    def __next__(self):
        for i in range(len(self)):
            yield i

    def __getitem__(self, indexer):
        nodo = self.__assit_getitem(indexer)
        if nodo:
            return nodo.valor
        else:
            raise StopIteration

    def __assist_repr(self, nodo=None, string="["):
        if not nodo:
            nodo = self.cabeza
        if nodo and nodo.siguiente:
            return self.__assist_repr(nodo.siguiente, string + str(nodo) + ",")
        else:
            if nodo:
                return string + str(nodo) + "]"
            else:
                return string + "]"

    def pop(self, i=None):
        if i is None:
            i = self.len - 1
        nodo = self.__find_nodo(i)
        valor = nodo.valor
        nodo_a = nodo.anterior
        nodo_s = nodo.siguiente
        if i == self.len - 1:
            self.cola = nodo_a
        elif i == 0:
            return self.popleft()
        if self.len == 1:
            self.cola = None
            self.cabeza = None
        if nodo_a:
            nodo_a.siguiente = nodo_s
        if nodo_s:
            nodo_s.anterior = nodo_a
        return valor

    def popleft(self, i=None):
        a = self.len
        if i is None:
            i = 0
        nodo = self.__find_nodo(i)
        valor = nodo.valor
        nodo_a = nodo.anterior
        nodo_s = nodo.siguiente
        if i == 0:
            self.cabeza = nodo_s
        elif self.len == 1:
            self.cola = None
            self.cabeza = None
        if nodo_a:
            nodo_a.siguiente = nodo_s
        if nodo_s:
            nodo_s.anterior = nodo_a
        return valor

    def __add__(self, other):
        temp = Lista()
        for i in self:
            temp.append(i)
        for i in other:
            temp.append(i)
        return temp

    def __repr__(self):
        return self.__assist_repr()

    def __str__(self):
        return self.__assist_repr()

    def sort(self):
        temp = Lista(*sorted(self, key=lambda x: x))
        for _ in range(self.len):
            self.pop()
        for i in temp:
            self.append(i)

    def insert(self, i, value):
        nodo = self.__find_nodo(i)
        if nodo:
            if nodo.anterior:
                nodo.anterior.siguiente = Nodo(value)
                nodo.anterior.siguiente.siguiente = nodo
                nodo.anterior.siguiente.anterior = nodo.anterior
                nodo.anterior = nodo.anterior.siguiente
            else:
                self.appendleft(value)
        elif i == self.len:
            self.append(value)
        else:
            raise IndexError

    def sort_cola(self):
        temp = Lista()
        while len(self) != 0:
            for i in range(self.len):
                if self[i] == max(self):
                    a = self.pop(i)
                    temp.append(a)
                    break
        while len(temp) != 0:
            self.append(temp.popleft())

    def reverse(self):
        n = self.len
        temp = Lista()
        for i in range(n):
            temp.append(self.pop())
        for i in temp:
            self.append(i)

    def copy(self):
        return Lista(*self)

    def __delitem__(self, key):
        self.pop(key)

    def __setitem__(self, key, value):
        self.__find_nodo(key).valor = value

    def __eq__(self, other):
        if self.len == other.len:
            nodo1 = self.cabeza
            nodo2 = self.cabeza
            for i in range(self.len):
                if not (nodo1.valor == nodo2.valor) or not nodo1:
                    return False
                nodo1 = nodo1.siguiente
                nodo2 = nodo2.siguiente
            return True
        else:
            return False

    def __lt__(self, other):
        if self[0] < other[0]:
            return True
        else:
            return False


if __name__ == "__main__":
    l = Lista(1, 2, 8, 4, 5)
    print(l)
    l.sort()
    print(l)
    l[0] = "a"
    print(l)
    j = l.copy()
    l.pop()
    print(j, l)
    l.reverse()
    print(l)
    l.insert(0, "shdahj")
    print(l)
    l.pop()
    l.popleft()
    l.append(5)
    l.append(-1)
    l.append(4)
    print(l)
    l.sort_cola()
    print(l)
