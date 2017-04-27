__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
#Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
#será penalizada con nota 1.0


class MetaPerson(type):
    def __new__(cls, name, bases, dic):
        if (name == "Chef" or name == "Client") and not(Person in bases):
            bases = (Person,)
        if name == "Chef":
            dic["restaurant"] = None
        if not "cook" in dic.keys() and name == "Chef":
            def cook(self):
                comida = Plate()
                dic["choose_drink"](self, comida)
                dic["choose_food"](self, comida)
                return comida
            dic["cook"] = cook
        if not "eat" in dic.keys() and name == "Client":
            def eat(self, plato):
                comida = 0
                bebida = 0
                if not isinstance(plato.drink, Drink):
                    if isinstance(plato.drink,Food) :  # Comida
                        comida += 1
                else:
                    bebida += 1
                if not isinstance(plato.food, Food):
                    if isinstance(plato.food, Drink):  # Comida
                        bebida += 1
                else:
                    comida += 1
                if comida == 0:
                    print("Me falta una comida")
                if bebida == 0:
                    print("Me falta una bebida")
                if bebida == 2:
                    print("Me dieron 2 bebidas")
                if comida == 2:
                    print("Me dieron 2 comida")
                if comida == 1 and bebida == 1:
                    # Se tomo el el promedio para la calidad
                    [print("Que delicia!") if (plato.drink.quality + plato.food.quality)/2 > 50 else print("Esto no es digno de mi paladar")]
            dic["eat"] = eat
        return super().__new__(cls, name, bases, dic)

class MetaRestaurant(type):
    instancias = {}
    def __new__(meta, name, bases, dic):
        def llega_cliente(self, cliente):
            if isinstance(cliente, Client):
                self.clients.append(cliente)
        def cliente_se_va(self,nombre):
            for cliente in self.clients:
                if cliente.name == nombre:
                    self.clients.remove(cliente)
        dic["llega_cliente"] = llega_cliente
        dic["cliente_se_va"] = cliente_se_va

        return super().__new__(meta, name, bases, dic)

    def __init__(cls, name, bases, dic):

        super().__init__(name,bases,dic)

    def __call__(cls, *args):
        if len(args)>= 2:
            if len(args)== 2:
                args = (*args, [])
            chefs = []

            for i in args[1]:
                if isinstance(i, Chef):
                    if i.restaurant is None:
                        i.restaurant = args[0]
                        chefs.append(i)
                    else:
                        if i.restaurant in cls.instancias.keys():
                            if len(cls.instancias[i.restaurant].chefs) != 1:
                                cls.instancias[i.restaurant].chefs.remove(i)
                                print("{} se fue de {} a {}".format(i.name,i.restaurant,args[0]))
                                i.restaurant = args[0]
                                chefs.append(i)
                        else:
                            i.restaurant = args[0]
                            chefs.append(i)
            if len(chefs) > 0:
                a = super().__call__(*(args[0],chefs,args[2]))
                cls.instancias[args[0]] = a
                chefs1 = [i.name for i in chefs]
                print("Restaurant creado exitosamente, los chefs son {}".format(chefs1))
                return a

###############################################################################
#De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients


    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass = MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients


    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
                Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
