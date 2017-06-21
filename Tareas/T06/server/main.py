import json
import os
import re
from json import JSONDecodeError
from random import choice

PORT = 49500
HOST = None
S_DIR = os.getcwd()
T_INDEX = {'int': int, 'str': str, 'float': float}

from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
from difflib import SequenceMatcher, diff_bytes, unified_diff
import sys
from uuid import getnode, uuid4


def validar_mail(s):
    pattern = "([a-z\.0-9]+[@][a-zA-z]+\.[a-z]+)"
    return bool(re.match(pattern, s))


def validate_user(s):
    pattern = "[A-Za-z0-9\_\-]{3,}"
    return bool(re.match(pattern, s))


class Server:
    def __init__(self, host=HOST, port=PORT):
        self.rooms = dict()
        self.onroom = set()
        self.block = Lock
        if not host:
            host = _LOCALHOST
        self.host = host
        self.port = port
        self.exit = False
        self.server_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(40)
        self.room_formats = dict()
        print("Server running at port {}".format(self.port))
        self.clients = dict()
        self.rooms_checker()  # Analiza el directorio songs -> escribir "rooms" en consola para ejecutar
        accept_daemon = Thread(target=self.accept, daemon=True, name="aceptartor", args=())
        accept_daemon.start()
        console = Thread(target=self.interpreter, daemon=True, name="Console", args=())
        console.start()
        accept_daemon.join()

    def interpreter(self):
        while True:
            quarry = input("{}:{} $ ".format(self.host, self.port)).split(" ")
            if len(quarry) == 1 and quarry[0] == "get":
                print("Users conected to server:")
                for client in self.clients.values():
                    print("User n°: {}".format(client))
            elif len(quarry) == 1 and quarry[0] == "rooms":
                self.rooms_checker()

    def accept(self):
        print("Server is accepting connections...")

        while not self.exit:
            new_client, address = self.server_socket.accept()
            listening_client = Thread(target=self.client_listener, args=(new_client,), daemon=True,
                                      name="{}:{}".format(*address))
            print("Listening client at adress: {}".format(listening_client.getName()))
            try:
                listening_client.start()
            except ConnectionResetError:
                print("Conection lost...")

    def rooms_checker(self, client=None):
        self.room_formats.clear()
        preformat = {'uuid': uuid4().int, 'users': 0, 'max': 20, 'segundos': 20, 'artist': []}
        rooms_dir = S_DIR + os.sep + "songs"
        rooms = os.listdir(rooms_dir)
        for room in rooms:
            room_format = preformat.copy()
            if os.path.isdir(rooms_dir + os.sep + room):
                songs = os.listdir(rooms_dir + os.sep + room)
                room_format['artist'] = list()
                for song in songs:
                    if re.match("[a-zA-Z\- ]+\.(wav)$", song):
                        header = re.split(" ?[-] ?", song)
                        room_format['artist'].append(header[0])
                if not (os.path.isfile(rooms_dir + os.sep + room + os.sep + "game.csv")) or not client:
                    uuid = uuid4().int
                    if not (os.path.isfile(rooms_dir + os.sep + room + os.sep + "game.csv")):
                        with open(rooms_dir + os.sep + "manifest.csv", "a") as file:
                            file.write("{},{}\n".format(room, uuid))
                    with open(rooms_dir + os.sep + room + os.sep + "game.csv", "w") as game:
                        game.write("player:int\n")
                else:
                    with open(rooms_dir + os.sep + "manifest.csv", "r") as data:
                        header = next(data)
                        uuid = next(filter(lambda x: room in x, data)).strip().split(",")[1]
                with open(rooms_dir + os.sep + room + os.sep + "game.csv", "r") as file:
                    header = next(file).strip()
                    long = len(file.readlines())
                room_format['users'] = long
                room_format['uuid'] = uuid
                self.room_formats.update({int(uuid): room_format.copy()})
                if not client:
                    self.management(room, uuid)
                    self.rooms.update({uuid: {'thread': Timer(function=self.management, interval=20, args=(room, uuid)),
                                              'name': room,
                                              'time_left': 20}})
                    self.rooms[uuid]['thread'].start()
                room_format.clear()
        if client:
            client.send(json.dumps({"status": "server_order",
                                    "option": "rooms",
                                    "rooms": self.room_formats}).encode("utf-8"))

    def management(self, room, uuid, *args):
        room_dir = os.path.join(os.getcwd(), "songs", room)
        songs = os.listdir(room_dir)
        songs.remove("game.csv")
        if "kernel.current" in songs:
            songs.remove("kernel.current")
        right_song = choice(songs)
        songs.remove(right_song)
        broadcast_songs = list()
        while len(broadcast_songs) < 3:
            if len(songs) >= 1:
                selected = choice(songs)
                songs.remove(selected)
                broadcast_songs.append(selected)
            else:
                broadcast_songs.append("I'm a potato")
        broadcast_songs.append(right_song)
        broadcast_artists = [re.split(" ?[-] ?", i)[0] + "\n" for i in broadcast_songs]
        with open(room_dir + os.sep + "kernel.current", "w") as file:
            file.write(right_song + "\n")
            file.writelines(broadcast_artists)

    @staticmethod
    def room(client: socket, room):
        manifest = os.path.join(os.getcwd(), "songs", "manifest.csv")
        with open(manifest, "r") as file:
            header = next(file).strip()
            game = next(filter(lambda x: str(room) in x, file)).strip().split(",")[0]
        songs = os.path.join(os.getcwd(), "songs", game)
        with open(songs + os.sep + "kernel.current", "r") as file:
            buttons = [name.strip() for name in file.readlines()[1:]]
        client.send(
            json.dumps({'status': 'server_display', 'order': 'show', 'room': room, 'buttons': buttons}).encode("utf-8"))

    def room_controller(self, client: socket, room: int):
        rooms_dir = S_DIR + os.sep + "songs"
        if not self.clients[client] in self.onroom:
            self.onroom.add(self.clients[client])
            with open(rooms_dir + os.sep + "manifest.csv", "r") as data:
                header = next(data).strip()
                name = next(filter(lambda x: str(room) in x, data)).strip().split(",")[0]
            with open(rooms_dir + os.sep + name + os.sep + "game.csv", "a") as game:
                game.write("{}\n".format(self.clients[client]))
            client.send(json.dumps({"status": "server_display", "order": "show", "room": room}).encode("utf-8"))

    def room_leaver(self, room_id, client: socket):
        rooms_dir = S_DIR + os.sep + "songs"
        with open(rooms_dir + os.sep + "manifest.csv", "r") as data:
            header = next(data)
            name = next(filter(lambda x: room_id in x, data)).strip().split(",")[0]
        with open(rooms_dir + os.sep + name + os.sep + "game.csv", "r") as file:
            header = next(file).strip()
            head = list()
            head.append(header)
            lines = [word.strip() for word in file.readlines()]
            if str(self.clients[client]) in lines:
                lines.pop(lines.index(str(self.clients[client])))
            new = "\n".join(head + lines) + "\n"
        with open(rooms_dir + os.sep + name + os.sep + "game.csv", "w") as file:
            file.write(new)
        self.onroom.remove(self.clients[client])
        pass

    def answer_check(self, client: socket, ans, room):
        rooms = os.path.join(S_DIR, "songs")
        with open(os.path.join(rooms, "manifest.csv"), "r") as manifest:
            header = next(manifest).strip()
            path = next(filter(lambda x: str(room) in x, manifest)).strip().split(",")[0]
        songs = os.path.join(rooms, path, "kernel.current")
        with open(songs, "r") as data:
            right = re.split(" ?[-] ?", next(data).strip())[0]
        if right == ans:
            with open(S_DIR + os.sep + "users.csv", "r") as database:
                index = next(database).strip().split(",").index("points")
                userline = next(filter(lambda x: str(self.clients[client]) in x, database))
                database.seek(0)
                new = database.readlines()
            user_index = new.index(userline)
            uinfo = new[user_index].strip().split(",")
            uinfo[index] = str(int(uinfo[index]) + 1)
            new[user_index] = ",".join(uinfo) + "\n"
            with open(S_DIR + os.sep + "users.csv", "w") as database:
                database.writelines(new)
            client.send(json.dumps({'status': 'answer_match', 'room': room, 'succes': True, 'ans': ans}).encode("utf-8"))
        else:
            client.send(json.dumps({'status': 'answer_match', 'room': room, 'succes': False, 'ans': ans}).encode("utf-8"))

    def client_listener(self, client_socket: socket):
        while True:
            try:
                mensaje = json.loads(client_socket.recv(2048).decode('utf-8'))
                if not ("option" in mensaje.keys() and (mensaje['option'] == "points" or mensaje['option'] == 'rooms')):
                    print('Datos recibidos en el server: {}'.format(mensaje))
                if client_socket in self.clients.keys():
                    if mensaje['status'] == 'msg':
                        print('Mensaje recibido: {}'.format(mensaje['content']))
                    elif mensaje['status'] == 'server_request':
                        if mensaje['option'] == 'points':
                            userid = self.clients[client_socket]
                            with open(os.getcwd() + os.sep + "users.csv") as database:
                                index = next(database).strip().split(",").index("points")
                                value = next(filter(lambda x: userid in x, database)).strip().split(",")[index]
                            client_socket.send(
                                json.dumps(
                                    {'status': 'server_response', "option": 'points', 'points': int(value)}).encode(
                                    "utf-8"))
                        elif mensaje['option'] == 'game_status':
                            print(mensaje)
                            pass
                        elif mensaje['option'] == 'name':
                            with open(S_DIR + os.sep + "users.csv", "r") as data:
                                header = next(data)
                                info = next(filter(lambda x: self.clients[client_socket] in x, data)).strip().split(",")
                                client_socket.send(
                                    json.dumps({"status": "server_response", "option": "name", 'name': info[1]}).encode(
                                        "utf-8"))
                        elif mensaje['option'] == 'rooms':
                            self.rooms_checker(client_socket)
                        elif mensaje['option'] == 'join':
                            self.room_controller(client_socket, mensaje['room'])
                    elif mensaje['status'] == 'game':
                        if mensaje['option'] == 'getbuttons':
                            self.room(client_socket, mensaje['room'])
                    elif mensaje['status'] == 'answer':
                        self.answer_check(client_socket, mensaje['content'], mensaje['room'])
                    elif mensaje['status'] == 'leave':
                        self.room_leaver(mensaje['room'], client=client_socket)
                    elif mensaje['status'] == 'disconnect':
                        client_socket.close()
                        self.clients.pop(client_socket, client_socket)
                        print("client disconnected")
                        break
                else:
                    if mensaje['status'] == 'login' or mensaje['status'] == 'signin':
                        self.login(client_socket, mensaje)
            except ConnectionResetError:
                print('Se perdio la comunicacion con el cliente')
                client_socket.close()
                if client_socket in self.clients:
                    if self.clients[client_socket] in self.onroom:
                        self.onroom.remove(self.clients[client_socket])
                    self.clients.pop(client_socket)
                break
            except UnicodeDecodeError:
                break
            except JSONDecodeError:
                break

    @staticmethod
    def send_archives(client: socket, file):
        client.send(json.dumps({"status": "file"}).encode('utf-8'))
        with open(file, "rb") as lectura:
            file = lectura.read()

        client.send(len(file).to_bytes(4, byteorder="big"))
        client.send(file)

    @staticmethod
    def recieve_compare_hash(client: socket, uuid):
        long = int.from_bytes(client.recv(4), byteorder="big")
        bits = b''
        while len(bits) < long:
            bits += client.recv(2048)
        if os.path.isfile(os.getcwd() + os.sep + "users_secure/{}".format(uuid)):
            with open(os.getcwd() + os.sep + "users_secure/{}".format(uuid), "rb") as passwd_hash:
                passwd = passwd_hash.read()
            if diff_bytes(unified_diff, bits, passwd):
                return True
        return False

    @staticmethod
    def new_user(client: socket, message: dict):
        uuid = uuid4().int
        with open(os.getcwd() + os.sep + "users.csv", "r") as database:
            header = next(database)
            data = database.read()
        if message["user"] in data:
            return client.send(json.dumps({"status": "signin", "success": False, "error": 1}).encode("utf-8"))
        elif message["email"] in data:
            return client.send(json.dumps({"status": "signin", "success": False, "error": 2}).encode("utf-8"))
        elif not validar_mail(message["email"]):
            return client.send(json.dumps({"status": "signin", "success": False, "error": 3}).encode("utf-8"))
        elif not validate_user(message["user"]):
            return client.send(json.dumps({"status": "signin", "success": False, "error": 4}).encode("utf-8"))
        else:
            client.send(json.dumps({"status": "signin", "success": True}).encode("utf-8"))
        while str(uuid) in data:
            uuid = uuid4().int
        with open(os.getcwd() + os.sep + "users.csv", "a") as database:
            database.write("\n{},{},{},{}".format(uuid, message["user"], message["email"], 0))
        long = int.from_bytes(client.recv(4), byteorder="big")
        bits = b''
        while len(bits) < long:
            bits += client.recv(2048)
        if not os.path.isfile(os.getcwd() + os.sep + "users_secure/{}".format(uuid)):
            with open(os.getcwd() + os.sep + "users_secure/{}".format(uuid), "wb") as passwd_hash:
                passwd_hash.write(bits)
        print("{} created with uuid {}".format(message["user"], uuid))

    def login(server, client: socket, login_message: dict):
        if login_message["status"] == "login" and "user" in login_message.keys():
            try:
                with open(os.getcwd() + os.sep + "users.csv", "r") as database:
                    user = next(filter(
                        lambda x: x.find(login_message["user"]) != -1,
                        database))
                user = user.strip().split(",")
                login_response = server.recieve_compare_hash(client, user[0])
                if not login_response:
                    print("User '{}' or password does not match".format(login_message["user"]))
                    client.send(json.dumps({"status": "login", "success": False, "error": 8}).encode("utf-8"))
                elif user[0] not in server.clients.values() and login_response:
                    server.clients[client] = user[0]
                    client.send(json.dumps({"status": "login", "success": True}).encode("utf-8"))
                    print("User: {} successfuly login".format(login_message["user"]))
                    return True
                else:
                    client.send(json.dumps({"status": "login", "success": False, "error": 6}).encode("utf-8"))
            except StopIteration:
                print("User '{}' or password does not match".format(login_message["user"]))
                if client in server.clients.keys():
                    server.clients.pop(client)
                client.send(json.dumps({"status": "login", "success": False, "error": 5}).encode("utf-8"))
        elif login_message["status"] == "signin" and "user" in login_message.keys() and "email" in login_message.keys():
            server.new_user(client, login_message)
            return False
        else:
            client.send(json.dumps({"status": "signin", "success": True}).encode("utf-8"))
        return False


if __name__ == '__main__':
    s = Server()
