class BaseDeDatos:
    def __init__(self, id="", lat="", lon="", **kwargs):
        self.id = str(id)
        self.lat = float(lat)
        self.lon = float(lon)


class Incendio(BaseDeDatos):
    def __init__(self, potencia="", fecha_inicio="", **kwargs):
        super().__init__(**kwargs)
        self.potenccia = int(potencia)
        self.fecha_inicio = str(fecha_inicio)


class Recurso(BaseDeDatos):
    def __init__(self, tipo="", velocidad="", autonomia="", delay="", tasa_extincion="", costo="", **kwargs):
        super().__init__(**kwargs)
        self.tipo = str(tipo)
        self.velocidad = int(velocidad)
        self.autonomia = int(autonomia)
        self.delay = int(delay)
        self.tasa_extincion = int(tasa_extincion)
        self.costo = int(costo)


class Meteorologia(BaseDeDatos):
    def __init__(self, fecha_inicio="", fecha_termino="", tipo="", valor="", radio=0, **kwargs):
        super().__init__(**kwargs)
        self.fecha_inicio = str(fecha_inicio)
        self.fecha_termino = str(fecha_termino)
        self.tipo = str(tipo)
        self.valor = str(valor)
        self.radio = int(radio)
