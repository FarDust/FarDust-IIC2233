super().__init__(**kwargs)#inicializa los argumentos de la clase superior


#Clases abstractas

from abc import ABCMEta, abstractmethod, abstractproperty

class Base(metaclass=ABCMEta):
	@abstractmethod
	def func_1(self):
		pass
	@abstractproperty
	def value(self):
		pass
		
class Hijo(Base):
	def __init__(self):
		pass