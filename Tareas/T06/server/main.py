import json
import os

PORT = 49500
HOST = None

from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
from difflib import SequenceMatcher, diff_bytes, unified_diff
import sys
from uuid import getnode, uuid4


class Server:
    def __init__(self, host=HOST, port=PORT):
        if not host:
            host = _LOCALHOST
        self.host = host
        self.port = port
        self.exit = False
        self.server_socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(40)
        print("Server running at port {}".format(self.port))
        self.clients = dict()
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

    def accept(self):
        print("Server is accepting connections...")

        while not self.exit:
            new_client, address = self.server_socket.accept()
            listening_client = Thread(target=self.client_listener, args=(new_client,), daemon=True,
                                      name="{}:{}".format(*address))
            print("Listening client at adress: {}".format(listening_client.getName()))
            try:
                if self.login(new_client):
                    listening_client.start()
            except ConnectionResetError:
                print("Conection lost...")

    def client_listener(self, client_socket: socket):
        print("Server connected to a client n° {}".format(self.clients[client_socket]))
        salir = False
        while not salir:
            try:
                mensaje = json.loads(client_socket.recv(2048).decode('utf-8'))
                print('Datos recibidos en el server: {}'.format(mensaje))
                if mensaje['status'] == 'msg':
                    print('Mensaje recibido: {}'.format(mensaje['content']))
                elif mensaje['status'] == 'disconnect':
                    client_socket.close()
                    print(client_socket)
            except ConnectionResetError:
                print('Se perdio la comunicacion con el cliente')
            except Exception as err:
                print("{}:{}".format(self.clients[client_socket],err))
            finally:
                client_socket.close()
                salir = True

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
        else:
            client.close()
        return False

    @staticmethod
    def new_user(client: socket, message: dict):
        uuid = uuid4().int
        with open(os.getcwd() + os.sep + "users.csv", "r") as database:
            data = database.read()
        if message["user"] in data:
            return client.send(json.dumps({"status": "signin", "success": False, "error": 1}).encode("utf-8"))
        elif message["email"] in data:
            return client.send(json.dumps({"status": "signin", "success": False, "error": 2}).encode("utf-8"))
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

    def login(server, client: socket):
        login_message = json.loads(client.recv(2048).decode("utf-8"))
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
                    client.close()
                elif user[0] not in server.clients.values() and login_response:
                    server.clients[client] = user[0]
                    print("User: {} successfuly login".format(login_message["user"]))
                    return True
                else:
                    print("User already in use -> disconnecting")
                    client.close()
            except StopIteration:
                print("User '{}' or password does not match".format(login_message["user"]))
                if client in server.clients.keys():
                    server.clients.pop(client)
                client.close()
        elif login_message["status"] == "signin" and "user" in login_message.keys() and "email" in login_message.keys():
            server.new_user(client, login_message)
            client.close()
            return False
        else:
            # Agregar a todas las lineas
            client.send(json.dumps({"status": "signin", "success": True}).encode("utf-8"))
            client.close()
        return False


if __name__ == '__main__':
    s = Server()
