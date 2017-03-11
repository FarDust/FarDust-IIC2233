class Figura:
	def __init__(self,a,b,c):
		pass
		
	@property
	def area(self):
		return("calculo del area")

figura1 = Figura(1,2,3)		
print(figura1.area) # NO figura1.area()
