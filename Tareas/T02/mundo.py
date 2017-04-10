from super_lista import Lista
from gobierno import Gobierno
from random import choice, randint, random
from os import mkdir
from infeccciones import Virus,Bacteria,Parasito


class Poblacion:
    def __init__(self, poblacion=0):
        self.limpios = int(poblacion)
        self.infectados = 0
        self.muertos = 0

    def infectar(self, n=1):
        if n > self.limpios:
            n = self.limpios
        self.infectados += n
        self.limpios -= n

    def matar(self, n):
        if n > self.infectados:
            n = self.infectados
        self.muertos += n
        self.infectados -= n

    def curar(self, n):
        if n > self.infectados:
            n = self.infectados
        self.limpios += n
        self.infectados -= n

    @property
    def vivos(self):
        return self.infectados + self.limpios

    @property
    def total(self):
        return self.limpios + self.infectados + self.muertos

    @property
    def per_infectados(self):
        return round((self.infectados / self.total) * 100, 2)

    @property
    def per_limpios(self):
        return round((self.limpios / self.total) * 100, 2)

    @property
    def per_muertos(self):
        return round((self.muertos / self.total) * 100, 2)

    def __repr__(self):
        return "Sanos: {}%,Infectados: {}%,Muertos: {}%".format(self.per_limpios, self.per_infectados, self.per_muertos)


class Pais:
    def __init__(self, nombre, poblacion):
        self.nombre = nombre
        self.poblacion = poblacion
        if poblacion.total > 0:
            self.fronteras = Lista()
            self.aeropuerto = None
            self.infeccion = None
            self.gobierno = Gobierno(self, self.fronteras)
            self.mascarillas = False
            self.cura = False
            # Encargado del manejo de entrada infeccion
            self.frontera = True

    def guardar(self):
        try:
            mkdir("current")
            print("Creando directorio 'current'")
        except:
            print("Directorio 'current' ya creado procediendo a guardar...")
        with open("current/{}_poblacion.csv".format(self.nombre), "w") as archivo:
            archivo.write("limpios: int,infectados: int,muertos: int\n")
            archivo.write("{},{},{}".format(self.poblacion.limpios, self.poblacion.infectados, self.poblacion.muertos))

        with open("current/{}.csv".format(self.nombre), "w") as archivo:
            archivo.write("pais: string,mascarillas: bool,cura: bool,frontera: bool\n")
            archivo.write("{},{},{},{}".format(self.nombre, self.mascarillas, self.cura, self.frontera))

    def cargar(self):
        with open("current/{}_poblacion.csv".format(self.nombre), "r") as archivo:
            linea = Lista(*Lista(*archivo.readlines())[1].strip().split(","))
            self.poblacion.limpios = int(linea[0])
            self.poblacion.infectados = int(linea[1])
            self.poblacion.muertos = int(linea[2])
            archivo.close()
        with open("current/{}.csv".format(self.nombre), "r") as archivo:
            linea = Lista(*Lista(*archivo.readlines())[1].strip().split(","))
            self.mascarillas = linea[0] is "True"
            self.cura = linea[1] is "True"
            self.frontera = linea[2] is "True"
            archivo.close()

    @property
    def estado(self):
        if self.poblacion.infectados == 0:
            return "limpio"
        elif self.poblacion.infectados > 0:
            return "infectado"
        else:
            return "muerto"

    def add_vertex(self, frontera):
        self.fronteras.append(frontera)

    def propagar(self):
        if self.estado == "infectado":
            for frontera in self.fronteras:
                try:
                    if frontera.abierto and random() < self.p_contagio:
                        if frontera.pais_a == self.nombre and frontera.pais_b_o.estado == "limpio":
                            frontera.pais_b_o.poblacion.infectar()
                            frontera.pais_b_o.infeccion = self.infeccion
                            with open("sucesos.txt", "a") as sucesos:
                                sucesos.write("Se infecto {}\n".format(frontera.pais_b_o.nombre))
                                sucesos.close()
                        elif frontera.pais_a_o.estado == "limpio":
                            frontera.pais_a_o.poblacion.infectar()
                            frontera.pais_a_o.infeccion = self.infeccion
                            with open("sucesos.txt", "a") as sucesos:
                                sucesos.write("Se infecto {}\n".format(frontera.pais_a_o.nombre))
                                sucesos.close()
                except:
                    pass
            for frontera in self.aeropuerto.vuelos:
                if frontera.abierto and random() < self.p_contagio:
                    try:
                        if frontera.pais_a == self.nombre and frontera.pais_b_o.estado == "limpio":
                            frontera.pais_b_o.poblacion.infectar()
                            frontera.pais_b_o.infeccion = self.infeccion
                            with open("sucesos.txt", "a") as sucesos:
                                sucesos.write("Se infecto {}\n".format(frontera.pais_b_o.nombre))
                                sucesos.close()
                        elif frontera.pais_a_o.estado == "limpio":
                            frontera.pais_a_o.poblacion.infectar()
                            frontera.pais_a_o.infeccion = self.infeccion
                            with open("sucesos.txt", "a") as sucesos:
                                sucesos.write("Se infecto {}\n".format(frontera.pais_a_o.nombre))
                            sucesos.close()
                    except:
                        pass

    @property
    def p_contagio(self):
        # Deberia ser 0.07 pero asi no llegan a abrirse los aeropuertos
        return min(
            (7 * self.poblacion.infectados) / (self.poblacion.vivos * len(self.fronteras + self.aeropuerto.vuelos)), 1)

    def propagar_cura(self):
        try:
            for vuelo in self.aeropuerto.vuelos:
                if vuelo.abierto:
                    if self.nombre == vuelo.pais_a_o.nombre:
                        vuelo.pais_b_o.infeccion = self.infeccion
                        vuelo.pais_b_o.cura = self.cura
                    elif vuelo.abierto:
                        vuelo.pais_a_o.infeccion = self.infeccion
                        vuelo.pais_a_o.cura = self.cura
        except:
            pass

    def calcular_curados(self):
        if self.poblacion.infectados < 1000:
            n = 0
            for _ in range(self.poblacion.infectados):
                if random() < 0.25 * self.infeccion.resistencia:
                    n += 1
            with open("sucesos.txt", "a") as sucesos:
                sucesos.write("Curados en {}: {}\n".format(self.nombre, n))
                sucesos.close()
            return n
        else:
            n = int(self.poblacion.infectados * 0.25 * self.infeccion.resistencia)
            with open("sucesos.txt", "a") as sucesos:
                sucesos.write("Curados en {}: {}\n".format(self.nombre, n))
                sucesos.close()
            return n

    def actualizar_datos(self):
        if self.cura and self.estado == "infectado":
            self.propagar_cura()
            self.poblacion.curar(self.calcular_curados())
        if self.poblacion.infectados > 0:
            self.expandir()
        for frontera in self.fronteras:
            if frontera.pais_a == self.nombre:
                frontera.statics_a = self.poblacion.per_infectados
            else:
                frontera.statics_b = self.poblacion.per_infectados
        if not self.frontera:
            for frontera in self.fronteras:
                if frontera.pais_a == self.nombre:
                    frontera.f_pais_a = False
                else:
                    frontera.f_pais_b = False
        if not self.aeropuerto.abierto:
            for ruta in self.aeropuerto.vuelos:
                ruta.abierto = False

    def expandir(self):
        infectados = randint(0, self.grandes_numeros)
        if self.mascarillas:
            infectados = int(infectados * 0.3 * self.infeccion.resistencia)
        with open("sucesos.txt", "a") as sucesos:
            sucesos.write("Infectados en {}: {}\n".format(self.nombre, infectados))
            sucesos.close()
        self.poblacion.infectar(infectados)

    def calcular_muertos(self, probabilidad):
        if self.poblacion.infectados < 100000:
            infectados = None
            for i in range(self.poblacion.infectados):
                if round(probabilidad ** i + 1, 2) != 0.0:
                    infectados = i + 1
                else:
                    break
            muertos = 0
            while infectados != 0:
                if random() < probabilidad ** infectados:
                    muertos = infectados
                    infectados = 0
                else:
                    infectados -= 1
            with open("sucesos.txt", "a") as sucesos:
                sucesos.write("Muertos en {}: {}\n".format(self.nombre, muertos))
                sucesos.close()
            self.poblacion.matar(muertos)
        else:
            n = int(self.poblacion.infectados * probabilidad)
            with open("sucesos.txt", "a") as sucesos:
                sucesos.write("Muertos en {}: {}\n".format(self.nombre, n))
                sucesos.close()
            self.poblacion.matar(n)

    @property
    def grandes_numeros(self):
        return 6 * max(int(self.poblacion.infectados), 1)

    @property
    def conection_number_e(self):
        return len(self.fronteras)

    @property
    def conection_number_a(self):
        return len(self.aeropuerto.vuelos)

    def __eq__(self, other):
        if self.nombre == other.nombre:
            return True
        else:
            return False

    def __repr__(self):
        return "{}: {}".format(self.nombre, self.fronteras + self.aeropuerto.vuelos)


class Mundo:
    def __init__(self, mundo=None, enfermedad=None):
        if mundo is None:
            self.mundo = Lista()
        self.mundo = mundo
        self.conectar()
        self.sugerencias = Lista()
        self.dias = 0
        self.enfermedad = enfermedad
        self.avance = Lista()
        for pais in mundo:
            pais.infeccion = self.enfermedad
        self.enfermedad_detectada = False
        self.critict_line = False

    def guardar(self):
        try:
            mkdir("current")
            print("Creando directorio 'current'")
        except:
            print("Directorio 'current' ya creado procediendo a guardar...")
        with open("current/mundo.csv", "w") as archivo:
            archivo.write("dias: int,enfermedad: type,detectada: bool,critict: bool, avance: Lista\n")
            archivo.write("{},{},{},{},{}\n".format(self.dias,type(self.enfermedad), self.enfermedad_detectada, self.critict_line,
                                                 self.avance))
            archivo.close()
        for pais in self.mundo:
            pais.guardar()
            for frontera in pais.fronteras:
                frontera.guardar()
            for vuelo in pais.aeropuerto.vuelos:
                vuelo.guardar()
        with open("current/random_airports.csv", "w") as archivo:
            archivo.write(open("random_airports.csv", "r").read())
            archivo.close()

    def cargar(self):
        with open("current/mundo.csv", "r") as archivo:
            linea = Lista(*Lista(*archivo.readlines())[1].strip().split(","))
            self.dias = int(linea[0])
            if "Bacteria" in linea[1]:
                self.enfermedad = Bacteria()
            elif "Virus" in linea[1]:
                self.enfermedad = Virus()
            elif "Parasito" in linea[1]:
                self.enfermedad = Parasito()
            for pais in self.mundo:
                pais.infeccion = self.enfermedad
            if linea[2] == "True":
                self.enfermedad_detectada = True
            else:
                self.enfermedad_detectada = False
            if linea[3] == "True":
                self.critict_line = True
            else:
                self.critict_line = False
            self.avance = Lista(*linea[4][1:-1].strip().split(","))
            for i in range(len(self.avance)):
                if self.avance[i] == "":
                    self.avance.pop(i)
                else:
                    self.avance[i] = float(self.avance[i])

        for pais in self.mundo:
            pais.cargar()
            for frontera in pais.fronteras:
                frontera.cargar()
            for vuelo in pais.aeropuerto.vuelos:
                vuelo.cargar()

    def conectar(self):
        for pais in self.mundo:
            for frontera in pais.fronteras:
                if pais:
                    if frontera.pais_a == pais.nombre:
                        frontera.pais_a_o = pais
                    else:
                        frontera.pais_b_o = pais
            for frontera in pais.aeropuerto.vuelos:
                if pais:
                    if frontera.pais_a == pais.nombre:
                        frontera.pais_a_o = pais
                    else:
                        frontera.pais_b_o = pais

    @property
    def pob_inf_t_per(self):
        return self.per_muertos + self.per_infeccion

    @property
    def poblacion_mundial(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.total
        return total

    @property
    def poblacion_infectada(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.infectados
        return total

    @property
    def poblacion_limpia(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.limpios
        return total

    @property
    def poblacion_muerta(self):
        total = 0
        for pais in self.mundo:
            total += pais.poblacion.muertos
        return total

    @property
    def per_muertos(self):
        return round((self.poblacion_muerta / self.poblacion_mundial) * 100, 2)

    @property
    def per_infeccion(self):
        return round((self.poblacion_infectada / self.poblacion_mundial) * 100, 2)

    @property
    def probabilidad_muerte(self):
        return min(max(0.2, self.dias ** 2 / 100000) * self.enfermedad.mortalidad, 1)

    @property
    def descubrimiento(self):
        # se agrego el 100 dado que el numero resultante era muy pequeño
        return min((self.enfermedad.visibilidad * self.poblacion_infectada * (self.poblacion_muerta ** 2) * 100) / (
            self.poblacion_mundial ** 3), 1)

    def avanzar_cura(self):
        if self.enfermedad_detectada and sum(self.avance) < 1:
            self.avance.append(self.poblacion_limpia / (2 * self.poblacion_mundial))
        elif sum(self.avance) > 1:
            temp = Lista()
            for pais in list((filter(lambda pais: pais.estado != "muerto", self.mundo))):
                temp.append(pais.cura)
            if True in temp:
                pass
            else:
                choice(self.mundo).cura = True
        else:
            if random() < self.descubrimiento:
                with open("sucesos.txt", "a") as sucesos:
                    sucesos.write("Enfermedad detectada: {}".format(type(self.enfermedad)))
                self.enfermedad_detectada = True

    def resumen_pais(self, nombre):
        nombre = nombre.lower().title()
        pais = Lista(*filter(lambda pais: pais.nombre == nombre, self.mundo))[0]
        salir = False
        while not salir:
            print("Resumen {} iniciado...".format(pais.nombre))
            print("1. estadisticas")
            print("2. acciones")
            print("x. salir")
            respuesta = input("Respuesta: ")
            pob = pais.poblacion
            if respuesta == "1":
                print("vivos: {}\ninfectados: {}\nmuertos: {}\n".format(pob.vivos, pob.infectados, pob.muertos))
            elif respuesta == "2":
                print(Lista(*(
                    str(sugerencia[1])[str(sugerencia[1]).find(".") + 1:str(sugerencia[1]).find(" of ")].replace("_",
                                                                                                                 " ")
                    for sugerencia in pais.gobierno.evaluar())))
            elif respuesta == "x":
                salir = True

    def resumen_global(self):
        salir = False
        while not salir:
            print("Resumen Global iniciado...")
            print("1. Paises limpios")
            print("2. Paises infectados")
            print("3. Paises muertos")
            print("x. salir")
            respuesta = input("Respuesta: ")
            print("Vivos: {}".format(self.poblacion_mundial - self.poblacion_muerta))
            print("Muertos: {}".format(self.poblacion_muerta))
            print("Infectados: {}".format(self.poblacion_infectada))
            print("Sanas: {}".format(self.poblacion_limpia))
            if respuesta is "1":
                print("Paises limpios:")
                for pais in self.mundo:
                    if pais.estado is "limpio":
                        print("-{}".format(pais.nombre))
            elif respuesta is "2":
                print("Paises infectados:")
                for pais in self.mundo:
                    if pais.estado is "infectado":
                        print("-{}".format(pais.nombre))
            elif respuesta is "3":
                print("Paises muertos:")
                for pais in self.mundo:
                    if pais.estado is "muerto":
                        print("-{}".format(pais.nombre))
            elif respuesta is "x":
                salir = True

    def muertes_infecciones(self):
        print("Muertos e infectados por dia: ")
        infecciones = Lista()
        moribundos = Lista()
        for dia in range(self.dias):
            with open("save/{}_sucesos.txt".format(dia), "r") as suceso:
                muertos = Lista(*(int(linea[linea.find(": ") + 2:linea.find("\n")]) for linea in
                                  Lista(*filter(lambda linea: "Muertos" in linea, suceso.readlines()))))
                suceso.seek(0)
                infectados = Lista(*(int(linea[linea.find(": ") + 2:linea.find("\n")]) for linea in
                                     Lista(*filter(lambda linea: "Infectados " in linea, suceso.readlines()))))
                infecciones += infectados
                moribundos += muertos
                print("dia {} |muertos: {}| infectados: {}".format(dia, sum(muertos), sum(infectados)))
                suceso.close()
        print("promedio de infecciones: {} por dia".format(int(sum(infecciones) / self.dias)))
        print("promedio de muertes: {} por dia".format(int(sum(moribundos) / self.dias)))

    def propagar(self):
        for pais in self.mundo:
            pais.propagar()

    def actualizar(self):
        with open("sucesos.txt", "w") as sucesos:
            sucesos.write("")
            sucesos.close()
        self.conectar()
        self.avanzar_cura()
        for pais in self.mundo:
            if pais.estado != "muerto":
                pais.actualizar_datos()
                if pais.poblacion.infectados > 0:
                    pais.calcular_muertos(self.probabilidad_muerte)
                pais.gobierno.noticias_infeccion(self.pob_inf_t_per)
                self.sugerencias += pais.gobierno.evaluar()
                self.sugerencias.sort_cola()
        if self.per_infeccion > 4 and not self.critict_line:
            for pais in self.mundo:
                pais.aeropuerto.abierto = True
                for vuelo in pais.aeropuerto.vuelos:
                    vuelo.abierto = True
            self.critict_line = True
            with open("sucesos.txt", "a") as sucesos:
                sucesos.write("aeropuertos abiertos\n".title())
                sucesos.write("dia {}\n".format(self.dias))
        for i in range(3):
            if len(self.sugerencias) > 0:
                self.sugerencias.popleft()[1]()
        if self.poblacion_infectada > 0:
            self.propagar()
        try:
            mkdir("save")
        except:
            pass
        with open("save/{}_sucesos.txt".format(self.dias), "w") as archivo:
            archivo.write(open("sucesos.txt", "r").read())
            archivo.close()
        with open("save/{}_mundo.csv".format(self.dias), "w") as archivo:
            archivo.write("enfermedad: type,detectada: bool,critict: bool, avance: Lista\n")
            archivo.write("{},{},{},{}\n".format(type(self.enfermedad), self.enfermedad_detectada, self.critict_line,
                                                 self.avance))
            archivo.close()
        self.dias += 1

    def __repr__(self):
        return "dia {} -> limpios: {}% ,infectados: {}% ,muertos: {}%".format(
            self.dias, round(self.poblacion_limpia * 100 / self.poblacion_mundial, 2),
            self.per_infeccion, self.per_muertos)
