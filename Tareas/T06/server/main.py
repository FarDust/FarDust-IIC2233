import json
import os

PORT = 49500
HOST = None

from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
from difflib import SequenceMatcher, diff_bytes, unified_diff
import sys
from uuid import getnode, uuid4

socket1 = socket(family=AF_INET, type=SOCK_STREAM)
socket2 = socket(family=AF_INET6, type=SOCK_STREAM)


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
        accept_daemon.join()

    def accept(self):
        print("Server is accepting connections...")

        while not self.exit:
            new_client, address = self.server_socket.accept()
            listening_client = Thread(target=self.client_listener, args=(new_client,), daemon=True,
                                      name="{}:{}".format(*address))
            print("Listening client at adress: {}".format(listening_client.getName()))
            if self.login(new_client):
                listening_client.start()
            pass

    def client_listener(self, client_socket: socket):
        print("Server connected to a new client...")
        salir = False
        while not salir:
            print(client_socket)
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
            finally:
                client_socket.close()
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
        else:
            client.close()
        return False

    @staticmethod
    def new_user(self,client):
        pass

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
        elif login_message["status"] == "signin":
            server.new_user(client)
        else:
            client.close()
        return False


if __name__ == '__main__':
    s = Server()
