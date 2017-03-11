__author__ = "cotehidalgov"
from abc import ABCMeta, abstractmethod

#Herencia
# -*- coding: utf-8 -*-

from random import randint, random, choice


class Plate:
	def __init__(self, food, drink):
		self.food = food
		self.drink = drink

class Food(metaclass = ABCMeta):
	def __init__(self, ingredients):
		self.ingredients = ingredients
		self.calidad = randint(50, 200)
		pass


#Se hace override en las subclases que hereda de Food
	def check_time(self):
		pass

class Drink:
	def __init__(self, tipo):
		self.tipo = tipo
		self.calidad= randint(50, 150)
		pass

class Personality(metaclass = ABCMeta):

	@abstractmethod
	def im_happy(self):
		pass
	@abstractmethod
	def im_mad(self):
		pass

	def react(self, quality):
		if quality >= 100:
			self.im_happy()
		else:
			self.im_mad()


class Person: # Solo los clientes tienen personalidad en esta actividad
	def __init__(self, name):
		self.name = name

class Restaurant:
	def __init__(self, chefs, clients):
		self.chefs = chefs
		self.clients = clients

	def start(self):
		for i in range(3): # Se hace el estudio por 3 dias
			print("----- Día {} -----".format(i + 1))
			plates = []
			for chef in self.chefs: 
				for j in range(3):  # Cada chef cocina 3 platos
					plates.append(chef.cook()) # Retorna platos de comida y bebida

			for client in self.clients:
				for plate in plates:
					client.eat(plate)


class Cool(Personality):


	def im_happy(self):
		print('Yumi! Que rico')

	def im_mad(self):
		print('Preguntare si puedo cambiar el plato')



class Hater(Personality):

	def im_happy(self):
		print('No esta malo, pero igual prefiero Pizza x2')

	def im_mad(self):
		print("Nunca mas vendre a Daddy Juan's!")




class Chef(Person):
    def __init__(self, name):
        super().__init__(name)
        self.ing_pizza = ['pepperoni', 'pina', 'cebolla', 'tomate', 'jamon', 'pollo']
        self.ing_ensalada = ['crutones', 'espinaca', 'manzana', 'zanahoria']


    def elegir_pizza(self):
        elecciones = [choice(self.ing_pizza), choice(self.ing_pizza), choice(self.ing_pizza)]
        return elecciones

    def elegir_ensalada(self):
        elecciones = [choice(self.ing_ensalada), choice(self.ing_ensalada)]
        return elecciones

    def cook(self):
        if random() >= 0.5:

            ing = ['salsa de tomate', 'queso']
            food = Pizza(ingredients = (ing + self.elegir_pizza()))

            if random() >= 0.5:
                drink = Soda(tipo = 'soda')
            else:
                drink = Jugo(tipo = 'jugo')
        else:

            food = Salad(ingredients = (['lechuga'] + self.elegir_ensalada()))
            if random() >= 0.5:
                drink = Soda(tipo='soda')
            else:
                drink = Jugo(tipo='jugo')

        return Plate(food, drink)




class Client(Person):
    def __init__(self, nombre, personalidad):
        super().__init__(nombre)
        self.personalidad = personalidad


    def eat(self, plate):

        calidad_promedio = (plate.food.calidad + plate.drink.calidad)/2
        self.personalidad.react(calidad_promedio)


class Pizza(Food):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = 'pizza'
        self.check_time()
        self.check_ingredients()

    def check_time(self):
        tiempo = randint(20,100)
        if tiempo >= 30:
            self.calidad -= 30

    def check_ingredients(self):
        if 'pepperoni' in self.ingredients:
            self.calidad += 50
        if 'pina' in self.ingredients:
            self.calidad -= 50


class Salad(Food):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tipo = 'ensalada'
        self.check_time()
        self.check_ingredients()

    def check_time(self):
        tiempo = randint(5, 60)
        if tiempo >= 30:
            self.calidad -= 30

    def check_ingredients(self):
        if 'crutones' in self.ingredients:
            self.calidad += 20
        if 'manzana' in self.ingredients:
            self.calidad -= 20


class Soda(Drink):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calidad -= 30

class Jugo(Drink):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.calidad += 30







if __name__ == '__main__':
	chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
	clients = [Client("Bastian", Hater()), Client("Flori", Cool()), 
				Client("Antonio", Hater()), Client("Felipe", Cool())]

	restaurant = Restaurant(chefs, clients)
	restaurant.start()





