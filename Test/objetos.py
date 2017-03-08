from abc import ABCMeta, abstractmethod

class Objetos(metaclass=ABCMeta):
#class Objetos:
	@abstractmethod
	def __init__(self,id = "",nombre = "",tipo = ""):
		self.nombre = nombre
		self.id = id 
		self.tipo = tipo

class Armas(Objetos):
	def __init__(self,dano = "",**kwargs):
		super().__init__(**kwargs)
		self.dano = dano
	
	def atacar(self):
		print("Se ha hecho {0} de daño".format(self.daño))
		
class Ballestas(Armas):
	def __init__(self,municion = "",**kwargs):
		super().__init__(**kwargs)
		self.municion = municion
		
print(Ballestas.__mro__)
p1 = Ballestas(nombre = "La rebanadora",id = "#0",tipo = "ballesta",dano = 5,municion = "flechas")