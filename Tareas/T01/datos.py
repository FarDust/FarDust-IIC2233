from os import mkdir
from math import pi
from tiempo import Tiempo


class BaseDeDatos:
    def __init__(self, id="", lat="", lon="", **kwargs):
        self.id = str(id)
        self.lat = float(lat)
        self.lon = float(lon)
        try:
            mkdir("datos")
        except:
            pass

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
        self.tasa_propagacion = 500  # metros/h
        self.prendido = True
        self.climas = {"VIENTO": None, "TEMPERATURA": None, "LLUVIA": None}
        try:
            mkdir("datos/incendios")
        except:
            pass
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
    def superficie_afectada(self):
        return 2 * pi * self.radio ** 2

    @superficie_afectada.setter
    def superficie_afectada(self,value):
        self.radio = (value/(2*pi))**(1/2)

    @property
    def puntos_poder(self):
        return self.superficie_afectada * self.potencia

    @puntos_poder.setter
    def puntos_poder(self, value):
        self.superficie_afectada = value/self.potencia

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
        self.tasa_propagacion = (value*1000)/self.tiempo_incendio_horas

    def actualizar(self):
        with open("datos/incendios/{}.anaf".format(self.id), "w") as archivo:
            archivo.write("prendio: " + str(self.prendido))
            archivo.close()


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
        self.puntos_poder_extintos = 0
        self.x = self.lat * 110
        self.y = self.lon * 110
        try:
            mkdir("datos/recursos")
        except:
            pass
        self.actualizar()

    @property
    def coeficiente_uso(self):
        if self.tiempo_trabajado is 0:
            return 0
        else:
            return self.tiempo_trabajado / self.tiempo_standby

    @property
    def coeficiente_eficiencia(self):
        return self.puntos_poder_extintos / self.tiempo_trabajado

    def movilizar(self, hora_salida, hora_actual, destino, clima):
        # destino es un objeto del tipo Incendio
        # destino tiene tupla de la forma (x,y) que indica el centro del incendio

        pass

    def apagar(self, incendio, tiempo):
        incendio.puntos_poder -= self.tasa_extincion*tiempo
        self.puntos_poder_extintos += self.tasa_extincion*tiempo
        return self.tasa_extincion*tiempo

    def actualizar(self):
        with open("datos/recursos/{}.anaf".format(self.id), "w") as archivo:
            archivo.write("estado: " + str(self.estado) + "\n")
            archivo.write("trabajado: " + str(self.tiempo_trabajado) + "\n")
            archivo.write("standby: " + str(self.tiempo_standby) + "\n")
            archivo.write("extinto: " + str(self.puntos_poder_extintos) + "\n")
            archivo.close()


class Meteorologia(BaseDeDatos):
    def __init__(self, fecha_inicio="", fecha_termino="", tipo="", valor="", radio=0, id="", lat="", lon="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.fecha_inicio = str(fecha_inicio)
        self.fecha_termino = str(fecha_termino)
        self.tipo = str(tipo)
        self.valor = float(valor)
        self.radio = int(radio)
