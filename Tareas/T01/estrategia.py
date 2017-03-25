from tiempo import Tiempo
from os import mkdir
from utiles import trigonometricas, distancia


class EstrategiaDeExtincion:
    def __init__(self, incendio, climas):
        self.incendio = incendio  # objeto de tipo Indencio de datos.py
        self.recursos_utilizados = []
        self.climas = climas
        for clima in climas.values():
            d = ((clima.lat - incendio.lat) ** 2 + (clima.lon - incendio.lon) ** 2) ** (1 / 2) * 110
            radios = incendio.radio + clima.radio / 1000
            if radios >= d:
                incendio.aumentar_tasa(clima)

    def cantidad_recursos(self, climas, recursos, movilizados=[]):
        universo = Tiempo()
        for i in recursos:
            pass

    def menu(self):
        pass

    def simular(self, recurso):
        universo = Tiempo()
        try:
            mkdir("datos/incendios/{}".format(self.incendio.id))
        except:
            pass
        log = open("datos/incendios/{}/simulacion_recurso_{}.txt".format(self.incendio.id, recurso.id), "w")
        d = distancia(recurso.pos[0], recurso.pos[1], self.incendio.pos[0], self.incendio.pos[1])
        respaldo = (self.incendio.fecha_actual, recurso.pos, self.incendio.puntos_poder)
        (x1, x2) = respaldo[1][0], self.incendio.pos[0]
        (y1, y2) = respaldo[1][1], self.incendio.pos[1]
        (cos, sen) = trigonometricas(x1, y1, x2, y2)
        log.write("".center(60, "=") + "\n")
        log.write(
            "fecha actual: {}, fecha_incendio: {}\n".format(self.incendio.fecha_actual, self.incendio.fecha_inicio))
        log.write("recurso id: {}".format(recurso.id) + " velocidad teorica: {} km/h\n".format(recurso.velocidad * 3.6))
        log.write("distancia al objetivo : {} Km\n".format(d))
        log.write("")
        (velocidad, horas, d1) = recurso.velocidad * 3.6, 0, d
        while d > self.incendio.radio and velocidad * 1.10 >= recurso.velocidad * 3.6:
            for clima in self.climas.values():
                dc = ((clima.lat - self.incendio.lat) ** 2 + (clima.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
                radios = self.incendio.radio + clima.radio / 1000
                if radios >= dc:
                    self.incendio.aumentar_tasa(clima)
            self.incendio.fecha_actual = universo.ultra_re_traducir(
                universo.ultra_traducir(self.incendio.fecha_actual) + (1 / 60))
            horas = (universo.ultra_traducir(self.incendio.fecha_actual)) - universo.ultra_traducir(respaldo[0])
            horas.as_integer_ratio()
            recurso.pos = (x1 + (recurso.velocidad * cos * 3.6 * horas),
                           y1 + (recurso.velocidad * sen * 3.6 * horas))
            d = distancia(recurso.pos[0], recurso.pos[1], self.incendio.pos[0], self.incendio.pos[1])
            velocidad = (d1 - d) / horas
            log.write("x: {} Km|y: {} Km\n".format(recurso.pos[0], recurso.pos[1]))
            log.write("Distancia: {} Km".format(d) + " tiempo: {} Horas".format(horas) +
                      " velocidad: {} km/h\n".format(velocidad))
            pass
        log.write("recurso id: {}".format(recurso.id) + "|horas totatales: " + str(
            universo.re_traducir_horas(horas)) + "horas\n")
        log.write("radio del incendio al llegar: {} Km \ndistancia al centro: {} Km\n".format(self.incendio.radio, d))
        log.write("".center(60, "=") + "\n")
        hora_llegada = horas
        h_trabajo = 0
        while recurso.delay > h_trabajo or self.incendio.puntos_poder < 0:
            for clima in self.climas.values():
                dc = ((clima.lat - self.incendio.lat) ** 2 + (clima.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
                radios = self.incendio.radio + clima.radio / 1000
                if radios >= dc:
                    self.incendio.aumentar_tasa(clima)
            self.incendio.fecha_actual = universo.ultra_re_traducir(
                universo.ultra_traducir(self.incendio.fecha_actual) + (1 / 60))
            horas = (universo.ultra_traducir(self.incendio.fecha_actual)) - universo.ultra_traducir(respaldo[0])
            horas.as_integer_ratio()
            h_trabajo = horas - hora_llegada
            d = distancia(recurso.pos[0], recurso.pos[1], self.incendio.pos[0], self.incendio.pos[1])
            if d > self.incendio.radio * 1.10:
                recurso.pos = (x1 + (recurso.velocidad * cos * 3.6 * horas),
                               y1 + (recurso.velocidad * sen * 3.6 * horas))
                log.write("Ajuste de posicion: ({},{})\n".format(recurso.pos))
            puntos_restados = recurso.apagar(self.incendio, (1 / 60))
            log.write("Puntos de poder del incedio: {}\nPuntos quitados: {}\n".format(self.incendio.puntos_poder,
                                                                                      puntos_restados))
            log.write("Tiempo: {} |horas trabajadas: {} horas\n".format(universo.re_traducir_horas(horas), h_trabajo))
        log.write("".center(60, "=") + "\n")
        """self.incendio.fecha_actual = respaldo[0]
        recurso.pos = respaldo[1]
        self.incendio.puntos_poder = respaldo[2]
        print("log {} listo!!!".format(recurso.id))"""
        log.close()


"""
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

for incendio in incendios:
    print(incendio)
    fechaActual = incendios[incendio].fecha_inicio
    incendios[incendio].fecha_actual = Tiempo().ultra_re_traducir(Tiempo().ultra_traducir(fechaActual) + 10)
    test = EstrategiaDeExtincion(incendios[incendio], climas)
    for i in recursos.values():
        test.simular(i)
        pass
"""
