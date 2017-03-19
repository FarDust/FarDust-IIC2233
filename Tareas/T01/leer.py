# leer v1.0.0


class Leer:
    def __init__(self, archivo):
        self.archivo = archivo
        pass

    @property
    def diccionario(self):
        with open(self.archivo, "r", encoding="utf8") as lectura:
            temp = lectura.readline().strip().split(",")
            lexicon = {}
            for i in temp:
                lexicon[(str(i[:i.find(":")]))] = i[i.find(":") + 1:]
            temp.clear()
            lectura.close()
        return lexicon

    @staticmethod
    def tipo(tipo, value):
        if tipo == "string":
            return str(value)
        elif tipo == "int":
            return int(value)
        elif tipo == "float":
            return float(value)
        else:
            return value

    @property
    def leer(self):
        directorio = {}
        with open(self.archivo, "r", encoding="utf8") as lectura:
            base = lectura.read()
            contador = -1
            lectura.seek(0)
            for _ in lectura:
                contador += 1
            for id in range(contador):
                id = str(id)
                temp = base[base.find("\n" + id):base.find("\n" + str(int(id) + 1))].strip().split(",")
                lexicon = {}
                n = 0
                for key, valor in self.diccionario.items():
                    lexicon[key] = self.tipo(valor, temp[n])
                    n += 1
                temp.clear()
                directorio[id] = lexicon
            lectura.close()
        return directorio

    def escribir(self, lexicon):
        for key in lexicon:
            if not (key in self.diccionario.keys()):
                print("Error: la llave {} no esta en el diccionario".format(key))
                return
        with open(self.archivo, "r+", encoding="utf8") as lectura:
            base = lectura.read()
            lectura.seek(0)
            linea = lectura.readline().strip().split(",")
            key_order = []
            escritura = ""
            for key in linea:
                key_order.append(lexicon[key.split(":")[0]])
                escritura = ",".join(key_order)
            if "\n" + lexicon["id"] + "," in base:
                # mostrar menu correspondiente
                # opciones = [sobreescribir, anular]
                print("no implementado")
                pass
            else:
                lectura.read()
                lectura.write(escritura + "\n")
            lectura.close()
            key_order.clear()
        pass

    def eliminar(self, id):
        id = str(id)
        with open(self.archivo, "r+", encoding="utf8") as lectura:
            base = lectura.read()
            if "\n{},".format(id) in base:
                temp = base.split("\n")
                temp.remove(base[base.find("\n" + id):base.find("\n" + str(int(id) + 1))].strip())
                lectura.close()
                with open(self.archivo, "w", encoding="utf8") as escritura:
                    escritura.write("\n".join(temp))
                temp.clear()
            else:
                print("Error: Elmento no existe")
                lectura.close()
        pass

    def remplazar(self, lexicon):
        id = str(lexicon["id"])
        with open(self.archivo, "r+", encoding="utf8") as lectura:
            base = lectura.read()
            lectura.seek(0)
            linea = lectura.readline().strip().split(",")
            key_order = []
            escritura = ""
            for key in linea:
                key_order.append(lexicon[key.split(":")[0]])
                escritura = ",".join(key_order)
            if "\n{},".format(id) in base:
                temp = base.split("\n")
                busqueda = base[base.find("\n" + id):base.find("\n" + str(int(id) + 1))].strip()
                temp.insert(temp.index(busqueda), escritura)
                temp.remove(busqueda)
                lectura.close()
                with open(self.archivo, "w", encoding="utf8") as remplazo:
                    remplazo.write("\n".join(temp))
                temp.clear()
            else:
                print("Error: Elemento no existe")
                lectura.close()
                # Opciones crear o no nuevo elemnto
            pass
        pass

    def completar(self, id):
        id = str(id)
        with open(self.archivo, "r", encoding="utf8") as lectura:
            base = lectura.read()
            temp = base[base.find("\n" + id):base.find("\n" + str(int(id) + 1))].strip().split(",")
            lexicon = {}
            n = 0
            for key, valor in self.diccionario.items():
                lexicon[key] = self.tipo(valor, temp[n])
                n += 1
            temp.clear()
            lectura.close()
        return lexicon


class Users(Leer):
    def __init__(self):
        super().__init__("usuarios.csv")


class Resources(Leer):
    def __init__(self):
        super().__init__("recursos.csv")


class Meteorology(Leer):
    def __init__(self):
        super().__init__("meteorogia.csv")


class Fire(Leer):
    def __init__(self):
        super().__init__("incendios.csv")
