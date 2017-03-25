from math import pi
from tiempo import Tiempo
from utiles import trigonometricas, distancia


class BaseDeDatos:
    def __init__(self, id="", lat="", lon="", **kwargs):
        self.id = str(id)
        self.lat = float(lat)
        self.lon = float(lon)

    @property
    def pos(self):
        return self.lat * 110, self.lon * 110

    @pos.setter
    def pos(self, valor):
        self.lat = valor[0] / 110
        self.lon = valor[1] / 110


class Incendio(BaseDeDatos):
    def __init__(self, potencia="", fecha_inicio="", id="", lat="", lon="", fecha="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.potencia = int(potencia)
        self.fecha_inicio = str(fecha_inicio)
        self.fecha_actual = str(fecha)
        self.fecha_apagado = None
        self.tasa_propagacion = 500  # metros/h
        self.climas = {"VIENTO": None, "TEMPERATURA": None, "LLUVIA": None}
        self.recursos = []
        self.puntos_i = self.puntos_poder
        self.actualizar()

    def disminuir_tasa(self):
        universo = Tiempo()
        for value in self.climas.values():
            if value and universo.ultra_traducir(self.fecha_actual) > universo.ultra_traducir(value.fecha_termino):
                if value.tipo == "VIENTO":
                    self.tasa_propagacion -= (value.valor * 1000) / 100
                elif value.tipo == "TEMPERATURA":
                    if value.valor > 30:
                        self.tasa_propagacion -= (value.valor - 30) * 25
                elif value.tipo == "LLUVIA":
                    self.tasa_propagacion += value.valor * 50
                self.climas[value.tipo] = None

    def aumentar_tasa(self, clima):
        universo = Tiempo()
        self.disminuir_tasa()
        if clima.tipo == "VIENTO":
            if self.climas[clima.tipo] is None or universo.ultra_traducir(clima.fecha_inicio) > universo.ultra_traducir(
                    self.climas[clima.tipo].fecha_inicio):
                self.climas["VIENTO"] = clima
                self.tasa_propagacion += (clima.valor * 1000) / 100
        elif clima.tipo == "TEMPERATURA":
            if self.climas[clima.tipo] is None or universo.ultra_traducir(clima.fecha_inicio) > universo.ultra_traducir(
                    self.climas[clima.tipo].fecha_inicio):
                self.climas["TEMPERATURA"] = clima
                if clima.valor > 30:
                    self.tasa_propagacion += (clima.valor - 30) * 25
        elif clima.tipo == "LLUVIA":
            if self.climas[clima.tipo] is None or universo.ultra_traducir(clima.fecha_inicio) > universo.ultra_traducir(
                    self.climas[clima.tipo].fecha_inicio):
                self.climas["LLUVIA"] = clima
                self.tasa_propagacion -= clima.valor * 50

    @property
    def porcentaje_extincion(self):
        return "{}%".format((1 - (self.puntos_poder / self.puntos_i)) * 100)

    @property
    def superficie_afectada(self):
        return 2 * pi * (self.radio / 1000) ** 2

    @superficie_afectada.setter
    def superficie_afectada(self, value):
        self.radio = 1000 * ((value / (2 * pi)) ** (1 / 2))

    def actualizar(self):
        if self.puntos_poder <= 0 and not self.fecha_apagado:
            self.fecha_apagado = self.fecha_actual

    @property
    def puntos_poder(self):
        return self.superficie_afectada * self.potencia

    @puntos_poder.setter
    def puntos_poder(self, value):
        self.superficie_afectada = value / self.potencia

    @property
    def tiempo_incendio_horas(self):
        universo = Tiempo()
        fecha_actual_horas = universo.re_traducir(self.fecha_actual.split(" ")[0]) * 24 + universo.traducir_horas(
            self.fecha_actual.split(" ")[1])
        fecha_inicio_horas = universo.re_traducir(self.fecha_inicio.split(" ")[0]) * 24 + universo.traducir_horas(
            self.fecha_inicio.split(" ")[1])
        return fecha_actual_horas - fecha_inicio_horas

    @property
    def radio(self):
        universo = Tiempo()
        self.disminuir_tasa()
        fecha_actual_horas = universo.re_traducir(self.fecha_actual.split(" ")[0]) * 24 + universo.traducir_horas(
            self.fecha_actual.split(" ")[1])
        fecha_inicio_horas = universo.re_traducir(self.fecha_inicio.split(" ")[0]) * 24 + universo.traducir_horas(
            self.fecha_inicio.split(" ")[1])
        if fecha_actual_horas - fecha_inicio_horas > 0.0:
            radio = (self.tasa_propagacion / 1000) * (fecha_actual_horas - fecha_inicio_horas)
            return radio
        else:
            return 0

    @radio.setter
    def radio(self, value):
        self.tasa_propagacion = (value * 1000) / self.tiempo_incendio_horas

    def __repr__(self):
        return "Incendio: {} |Porcentaje de extincion: {}|" \
               "Fecha de inicio: {}|Recursos: {} ".format(self.id, self.porcentaje_extincion, self.fecha_inicio,
                                                          self.recursos)


class Recurso(BaseDeDatos):
    def __init__(self, tipo="", velocidad="", autonomia="", delay="", tasa_extincion="", costo="",
                 id="", lat="", lon="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.tipo = str(tipo)
        self.velocidad = int(velocidad)
        self.autonomia = int(autonomia)
        self.delay = int(delay)
        self.tasa_extincion = int(tasa_extincion)
        self.costo = int(costo)
        self.tiempo_trabajado = 0
        self.tiempo_standby = 0
        self.estado = "standby"
        self.movilizado = 0
        self.puntos_poder_extintos = 0
        self.incendio = None
        self.x = self.lat * 110
        self.y = self.lon * 110

    @property
    def trabajo_restante(self):
        return self.autonomia - self.tiempo_trabajado

    @property
    def coeficiente_uso(self):
        if self.tiempo_trabajado is 0:
            return 0
        else:
            return self.tiempo_trabajado / self.tiempo_standby

    @property
    def coeficiente_eficiencia(self):
        if self.tiempo_trabajado is 0:
            return 0
        return self.puntos_poder_extintos / self.tiempo_trabajado

    def asignar_incendio(self, incendio):
        self.incendio = incendio

    def movilizar(self, climas):
        # destino es un objeto del tipo Incendio
        # destino tiene tupla de la forma (x,y) que indica el centro del incendio
        self.movilizado += 1
        universo = Tiempo()
        for clima in climas.values():
            d = ((clima.lat - self.incendio.lat) ** 2 + (clima.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
            radios = self.incendio.radio + clima.radio / 1000
            if radios >= d:
                self.incendio.aumentar_tasa(clima)
        d = distancia(self.pos[0], self.pos[1], self.incendio.pos[0], self.incendio.pos[1])
        respaldo = (self.incendio.fecha_actual, self.pos, self.incendio.puntos_poder)
        (x1, x2) = respaldo[1][0], self.incendio.pos[0]
        (y1, y2) = respaldo[1][1], self.incendio.pos[1]
        (velocidad, horas, d1) = self.velocidad * 3.6, 0, d
        (cos, sen) = trigonometricas(x1, y1, x2, y2)
        while d > self.incendio.radio and velocidad * 1.10 >= self.velocidad * 3.6:
            for clima in climas.values():
                dc = ((clima.lat - self.incendio.lat) ** 2 + (clima.lon - self.incendio.lon) ** 2) ** (1 / 2) * 110
                radios = self.incendio.radio + clima.radio / 1000
                if radios >= dc:
                    self.incendio.aumentar_tasa(clima)
            self.incendio.fecha_actual = universo.ultra_re_traducir(
                universo.ultra_traducir(self.incendio.fecha_actual) + (1 / 60))
            horas = (universo.ultra_traducir(self.incendio.fecha_actual)) - universo.ultra_traducir(respaldo[0])
            horas.as_integer_ratio()
            self.pos = (x1 + (self.velocidad * cos * 3.6 * horas),
                        y1 + (self.velocidad * sen * 3.6 * horas))
            d = distancia(self.pos[0], self.pos[1], self.incendio.pos[0], self.incendio.pos[1])
            velocidad = (d1 - d) / horas
        self.incendio.fecha_actual = respaldo[0]
        self.pos = respaldo[1]
        return horas

    def apagar(self, incendio, tiempo):
        incendio.puntos_poder -= self.tasa_extincion * tiempo
        self.puntos_poder_extintos += self.tasa_extincion * tiempo
        return self.tasa_extincion * tiempo

    def __lt__(self, other):
        if self.coeficiente_uso <= other.coeficiente_uso:
            return True
        else:
            return False

    def __repr__(self):
        string = "estado: {}, posicion(lat,lon): ({},{}))".format(self.estado, self.lat, self.lon)
        if self.estado != "standby":
            string += "\nTiempo trabajado: {},Tiempo de Trabajo restante: {}".format(self.tiempo_trabajado,
                                                                                     self.trabajo_restante)
        if self.estado == "viajando":
            string += "\nDistancia al objetivo: {}".format(distancia(self.pos[0], self.pos[1],
                                                                     self.incendio.pos[0], self.incendio.pos[1]))
        return string


class Meteorologia(BaseDeDatos):
    def __init__(self, fecha_inicio="", fecha_termino="", tipo="", valor="", radio=0, id="", lat="", lon="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.fecha_inicio = str(fecha_inicio)
        self.fecha_termino = str(fecha_termino)
        self.tipo = str(tipo)
        self.valor = float(valor)
        self.radio = int(radio)
