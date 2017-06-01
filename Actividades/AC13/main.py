import datetime
from os import listdir, mkdir
from json import JSONEncoder, JSONDecoder, dumps, loads, load, dump
from os.path import join as union
from random import random, randint
from pickle import dumps as morph
from pickle import loads as cargar

try:
    mkdir("secure_db")
    mkdir("secure_db/usr")
    mkdir("secure_db/msg")
except Exception:
    pass


def identifier():
    i = 0
    while True:
        yield str(i) + "#iic2233-" + str(randint(0, i))
        i += 1


class Usuario:
    identifiers = identifier()

    def __init__(self, name: str = "", contacts: list = None, phone_number: int = 0, **kwargs):
        self.id = next(self.identifiers)
        if not contacts:
            contacts = list()
        self.contacts = contacts
        self.name = name
        self.phone_number = phone_number

    def __repr__(self):
        return str(self.phone_number)


class Mensaje:
    def __init__(self, send_to=0, content="", send_by=0, last_view_date="", date="", **kwargs):
        self.send_to = send_to
        self.content = content
        self.send_by = send_by
        self.last_view_date = last_view_date
        self.date = date

    def __repr__(self):
        return str(self.content)

    def __str__(self):
        return  str(self.content)

    def __getstate__(self):
        nueva = self.__dict__
        nueva.update({"content": caesar_cipher(self.content, self.send_by)})
        return nueva

    def __setstate__(self, state):
        state.update({"last_view_date": datetime.datetime.now().isoformat()})
        self.__dict__ = state

    pass


class Encoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Usuario):
            return self.diction(o)

        return super().default(o)

    @staticmethod
    def diction(o):
        return {"name": o.name, "phone_number": o.phone_number, "contacts": o.contacts}


def read_all(main):
    from os import listdir
    root = listdir(main)
    objects = dict()
    types = {"usr": Usuario, "msg": Mensaje}
    for i in types.keys():
        objects[i] = set()
    for i in root:
        if i in types.keys():
            [objects[i].add(load(open(main + "/" + i + "/" + obj, "r"), object_hook=lambda usr: types[i](**usr))) for
             obj in listdir(main + "/" + i)]
    return objects


def usuarios():
    return list(read_all("db")["usr"])


def mesages():
    return list(read_all("db")["msg"])


def indexar(msgs, usrs):
    for msg in msgs:
        usr = next(filter(lambda usr: msg.send_by == usr.phone_number, usrs))
        if msg.send_to not in usr.contacts:
            usr.contacts.append(msg.send_to)


def caesar_cipher(string, number):
    new_one = ""
    abc = list("abcdefghijklmnopqrstuvwxyz")
    for caracter in string:
        if caracter in abc:
            new_one += chr((ord(caracter) + number) % 26)
        else:
            new_one += caracter
    return new_one


def guardar_user(usr: Usuario):
    with open("secure_db/usr/" + usr.id + ".json", "w") as json:
        json.write(dumps(usr, cls=Encoder))


msg_indentifiers = identifier()


def guardar_msg(msg: Mensaje):
    with open("secure_db/msg/" + next(msg_indentifiers) + ".iic2233", "wb") as archivo:
        archivo.write(morph(msg))


if __name__ == '__main__':
    users = usuarios()
    msgs = mesages()
    indexar(msgs, users)
    for i in users:
        guardar_user(i)
    for i in msgs:
        guardar_msg(i)
    with open("secure_db/msg/0#iic2233-0.iic2233", "rb") as mensaje:
        objeto = cargar(mensaje.read())
    print(objeto.__dict__)