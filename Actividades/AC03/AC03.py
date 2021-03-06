# AC03 -Actividad en clases
from collections import deque
from random import choice

class Camion:
    def __init__(self, capacidad_maxima, urgencia):
        self.capacidad_maxima = int(capacidad_maxima)
        self.urgencia = urgencia
        self.productos = []
        self.llenado = False

    # modificar len(productos)
    def agregar_producto(self, producto):
        if self.peso_acumulado + producto.peso < self.capacidad_maxima:
            self.productos.append(producto)
        else:
            print("Capacidad maxima alcanzada")

    @property
    def peso_acumulado(self):
        n = 0
        for producto in self.productos:
            n += producto.peso
        return n

    def __str__(self):
        string = ""
        dic = {}
        for producto in self.productos:
            if not(producto.tipo in dic):
                dic[producto.tipo] = 1
            else:
                dic[producto.tipo] += 1
        for tipo, cantidad in dic.items():
            string += "{} : {}\n".format(tipo, cantidad)
        return string


class CentrosDistribucion:
    def __init__(self):
        self.fila = deque()
        self.bodega = {}
        self.numeroCamiones = 0
        with open("camiones.txt","r") as camiones:
            for camion in camiones:
                camion = camion.strip()
                atributos = camion.split(",")
                self.recibir_camion(Camion(atributos[0],atributos[1]))
            camiones.close()
        with open("productos.txt","r") as productos:
            for producto in productos:
                producto = producto.strip()
                atributos = producto.split(",")
                self.recibir_donacion(Producto(atributos[0],atributos[1],atributos[2]))
            camiones.close()
        print(self.bodega)
        for i in range(len(self.fila)):
            self.rellenar_camion()
            self.enviar_camion()


    # Prioridad 10 mayor que todas
    def recibir_camion(self, camion):
        if len(self.fila) is 0:
            self.fila.append(camion)
        else:
            for i in range(len(self.fila)):
                if self.fila[i].urgencia > camion.urgencia:
                    self.fila.insert(i, camion)
                else:
                    self.fila.append(camion)
                    break

    def rellenar_camion(self):
        for almacen in self.bodega.values():
            for pila in almacen.values():
                if pila != []:
                    if pila[-1].peso + self.fila[0].peso_acumulado < self.fila[0].capacidad_maxima:
                        self.fila[0].agregar_producto(pila.pop())

        self.fila[0].llenado = True


    def enviar_camion(self):
        if(self.fila[0].llenado == True):
            print("camion numero {} enviado\n contenido {}".format(self.numeroCamiones,self.fila[0]))
            self.fila.popleft()
            self.numeroCamiones += 1
        else:
            print("Camion no se ha llenado aun")
        pass

    def mostrar_productos_por(self,tipo):
        string = "mostrando objetos del tipo: ".format(tipo)
        for i in self.bodega[tipo].values():
            for j in i:
                string += "{}\n".format(j.nombre)
        pass

    def recibir_donacion(self, *args):
        for producto in args:
            if producto.tipo in self.bodega:
                if producto.nombre in self.bodega[producto.tipo]:
                    self.bodega[producto.tipo][producto.nombre].append(producto)
                else:
                    self.bodega[producto.tipo][producto.nombre] = [producto]
            else:
                self.bodega[producto.tipo] = {producto.nombre: [producto]}

class Producto:
    def __init__(self,tipo, nombre, peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = int(peso)

    def __eq__(self, other):
        if(self.tipo == other.tipo) and (self.nombre == other.nombre):
            return True
        else:
            return False

    def __repr__(self):
        return self.nombre

Bodegin = CentrosDistribucion()
