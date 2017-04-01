# Empieza la fiesta
from leemundo import generar_aeropuertos, generar_fronteras, generar_paises
from mundo import Mundo

planeta = Mundo(generar_aeropuertos(generar_fronteras(generar_paises())))

planeta.actualizar()

planeta.mundo[0].poblacion.infectados = 74000000

planeta.actualizar()

l = planeta.mundo[0].gobierno.evaluar()
l[0][1]()
print("")
planeta.mundo[3].gobierno.evaluar()
