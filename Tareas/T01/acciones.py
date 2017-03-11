#Acciones v1.0.0

class Accion:
	def __init__(self,usuario):
		usuario.permiso.sort()
		self.permiso = usuario.permiso[-1]

	def crear_usuario(self,name,password)
		pass
		
class AgregarUsuario(Accion):
	def __init__(self):
		super().__init__()
		if(permiso >= "ANAF"):
			self.crear_usuario()
			
		else:
			print("ERROR: No tienes los permisos necesarios pra realizar esta accion")
			return 

class ConsultaBasica(Accion):
	def __init__():
		pass