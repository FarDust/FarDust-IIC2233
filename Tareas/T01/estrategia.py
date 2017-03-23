from menu import Basico
from datos import Incendio, Recurso, Meteorologia
from leer import Resources, Fire, Meteorology
from tiempo import Tiempo


class EstrategiaDeExtincion:
    def __init__(self, incendio, climas):
        self.incendio = incendio  # objeto de tipo Indencio de datos.py
        self.recursos_utilizados = []
        for clima in climas.values():
            d = ((clima.lat - incendio.lat) ** 2 + (clima.lon - incendio.lon) ** 2) ** (1 / 2) * 110
            radios = incendio.radio + clima.radio / 1000
            if radios >= d:
                incendio.aumentar_tasa(clima)

    def cantidad_recursos(self, climas, recursos, movilizados=[]):
        universo = Tiempo()
        for i in recursos:
            pass

    def simular(self, recurso):
        universo = Tiempo()
        d = ((recurso.lat - self.incendio.lat) ** 2 + (recurso.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
        respaldo = (self.incendio.fecha_actual, recurso.pos)
        print(d * 1000 // 1, 0 / 60)
        while not (d*1000//1 <= self.incendio.radio*1000):
            d1=d
            self.incendio.fecha_actual = universo.ultra_re_traducir(
                universo.ultra_traducir(self.incendio.fecha_actual) + 1 / 60)
            horas = (universo.ultra_traducir(self.incendio.fecha_actual)) - universo.ultra_traducir(respaldo[0])
            horas.as_integer_ratio()
            x1 = recurso.pos[0]
            x2 = self.incendio.pos[0]
            y1 = recurso.pos[1]
            y2 = self.incendio.pos[1]
            recurso.pos = (x1 + (x2 - x1) * ((recurso.velocidad * 60 * horas) / 1000),
                           y1 + (y2 - y1) * ((recurso.velocidad * 60 * horas) / 1000))
            d = ((recurso.lat - self.incendio.lat) ** 2 + (recurso.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
            velocidad = (d - d1) / horas
            print(d * 1000 // 1, horas / 60,"velocidad: {}km/h".format(velocidad))
        print(d * 1000 // 1, horas / 60)
        print("recurso id: {}".format(recurso.id),"|horas totatales:",universo.re_traducir_horas(horas),"horas")
        self.incendio.fecha_actual = respaldo[0]
        recurso.pos = respaldo[1]


fechaActual = "2017-03-24 08:32:00"
recursos = {}
incendios = {}
climas = {}

# Instanciar recursos
for key, value in Resources().leer.items():
    recursos[key] = Recurso(**value)

# Instanciar incendios
for key, value in Fire().leer.items():
    incendios[key] = Incendio(fecha=fechaActual, **value)

# Instaciar climas
for key, value in Meteorology().leer.items():
    climas[key] = Meteorologia(**value)

test = EstrategiaDeExtincion(incendios["99"], climas)
for i in recursos.values():
    test.simular(i)
    pass
