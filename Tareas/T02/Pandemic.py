# Empieza la fiesta
from leemundo import generar_aeropuertos, generar_fronteras, generar_paises
from mundo import Mundo
from infeccciones import Virus

planeta = Mundo(generar_aeropuertos(generar_fronteras(generar_paises())),Virus())
n = 0
while True:
    planeta.actualizar()


