from os import mkdir
class BaseDeDatos:
    def __init__(self, id="", lat="", lon="", **kwargs):
        self.id = str(id)
        self.lat = float(lat)
        self.lon = float(lon)
        try:
            mkdir("datos")
        except:
            pass


class Incendio(BaseDeDatos):
    def __init__(self, potencia="", fecha_inicio="",id="", lat="", lon="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.potenccia = int(potencia)
        self.fecha_inicio = str(fecha_inicio)
        self.prendido = True
        try:
            mkdir("datos/incendios")
        except:
            pass
        self.actualizar()

    def actualizar(self):
        with open("datos/incendios/{}.anaf".format(self.id), "w") as archivo:
            archivo.write("prendio: "+str(self.prendido))
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


class Meteorologia(BaseDeDatos):
    def __init__(self, fecha_inicio="", fecha_termino="", tipo="", valor="", radio=0, id="", lat="", lon="", **kwargs):
        super().__init__(id=id, lat=lat, lon=lon)
        self.fecha_inicio = str(fecha_inicio)
        self.fecha_termino = str(fecha_termino)
        self.tipo = str(tipo)
        self.valor = str(valor)
        self.radio = int(radio)
