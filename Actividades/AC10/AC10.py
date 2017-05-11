from threading import Thread, Lock
from random import randint, expovariate, choice
from time import time


def termo():
    i = 0
    while True:
        yield i
        i += 1


class Laberinto:
    def __init__(self):
        self.personas = []
        with open("laberinto.txt", "r") as archivo:
            self.init = next(archivo).strip()
            self.out = next(archivo).strip()
            self.piezas = [Piezas(str(i)) for i in range(int(self.init), int(self.out) + 1)]
            for j in archivo:
                for i in self.piezas:
                    if j.strip().split(",")[0] == i.id:
                        i.conexiones.append(self.piezas[int(j.strip().split(",")[1]) - 1])


class Piezas:
    def __init__(self, id):
        self.id = id
        self.lock = Lock()
        self.conexiones = []

    def __repr__(self):
        return "pieza {}".format(self.id)


class Persona(Thread):
    ident = termo()

    def __init__(self, inicio):
        super().__init__()
        self.id = next(self.ident)
        self.hp = randint(80, 120)
        self.pieza_actual = inicio
        self.resistencia = randint(1, 3)
        self.daemon = True
        self.start()

    def run(self):
        last_election = time()
        tiempo_inicial = time()
        inicial = self.pieza_actual.id
        infeccion = Thread(target=self.infeccion, daemon=True)
        infeccion.start()
        while self.hp > 0:
            t_actual = time()
            if self.pieza_actual.id == "60":
                log("{} - {} - {}".format(self,time(),time()-tiempo_inicial))
            if t_actual - last_election > randint(1, 3):
                if len(self.pieza_actual.conexiones):
                    eleccion = choice(self.pieza_actual.conexiones)
                    if not eleccion.id == "60":
                        eleccion.lock.acquire()
                    print("{}: {} -> {} | hp = {}".format(self, self.pieza_actual, eleccion, round(self.hp, 2)))
                    if self.pieza_actual.id != inicial:
                        self.pieza_actual.lock.release()
                    self.pieza_actual = eleccion
                    last_election = t_actual
        print("{}: Murio :( en la {}".format(self, self.pieza_actual))
        pass

    def infeccion(self):
        t_actual = time()
        while self.hp > 0 and self.pieza_actual.id != "60":
            tf = time()
            self.hp -= (6 - self.resistencia) * (tf - t_actual)
            t_actual = tf

    def __repr__(self):
        return "Persona {}".format(self.id)


class Barrendero(Thread):
    def __init__(self, laberinto):
        super().__init__()
        self.laberinto = laberinto
        self.daemon = True
        self.start()

    def run(self):
        self.contador = 0
        while True:
            for persona in self.laberinto.personas:
                if not persona.isAlive():
                    print("cadaver de la {} removid@".format(persona))
                    self.contador += 1
                    self.laberinto.personas.remove(persona)


class Spawner(Thread):
    def __init__(self, laberinto):
        super().__init__()
        self.laberinto = laberinto
        self.daemon = True
        self.start()

    def run(self):
        eventos = []
        t0 = time()
        eventos.append(time() - t0 + round(expovariate(1 / 5) + 0.5))
        while len(list(filter(lambda x: x.pieza_actual.id == self.laberinto.out, self.laberinto.personas))) < 3:
            eventos.sort()
            if time() - t0 >= eventos[0]:
                self.crear_persona()
                print("{} entro al laberinto en t = {}".format(self.laberinto.personas[-1], time() - t0))
                eventos.append(time() - t0 + round(expovariate(1 / 5) + 0.5))
                eventos.pop(0)
        pass

    def crear_persona(self):
        self.laberinto.personas.append(
            Persona(list(filter(lambda x: x.id == self.laberinto.init, (i for i in self.laberinto.piezas)))[0]))


def log(texto):
    with open("registro_suscesos.txt", "a") as log:
        log.write(texto + "\n")

t0 = time()
l = Laberinto()
k = Spawner(l)
barrendero = Barrendero(l)
k.join()
log("Muertos: {}".format(barrendero.contador))