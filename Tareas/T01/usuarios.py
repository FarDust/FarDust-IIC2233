#Usuarios v1.0.0

from abc import ABCMeta,abstractmethod

class Usuario:
	def __init__(self,nombre,password):
		self.nombre = nombre
		self.password = password
		self.permisos = []
	
class Root(Usuario):
	def __init__(self,password):
		super().__init__("root",password)
		self.permisos.append("root")
		self.permisos.sort()
		pass
		
class ANAF(Usuario):
	def __init__(self):
		super().__init__(nombre,password)
		self.permisos.append("ANAF")
		self.permisos.sort()
		pass
		
class Terreno(Usuario):
	def __init__(self):
		super().__init__(nombre,password)
		self.permisos.append("terreno")
		self.permisos.sort()
		pass