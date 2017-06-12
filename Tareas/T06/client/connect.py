import json
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
import sys
from uuid import getnode, uuid4

from PyQt5.QtCore import QCryptographicHash, pyqtSignal, QObject

# socket1 = socket(family=AF_INET, type=SOCK_STREAM)
# socket2 = socket(family=AF_INET6, type=SOCK_STREAM)

sha512 = 6
sha3_512 = 10

PORT = 49500
HOST = None


class Client(QObject,Thread):
    messages = pyqtSignal(dict)

    def __init__(self, host=HOST, port=PORT):
        super().__init__()
        if host is None:
            host = _LOCALHOST
        self.host = host
        self.port = port
        self.v4socket = socket(family=AF_INET, type=SOCK_STREAM)

    def getInteface(self, interface):
        self.messages.connect(interface.receiver)

    def receiver(self, arguments: dict):
        self.getInteface(self.sender())
        try:
            if arguments["status"] == "login":
                self.login(**arguments)
            elif arguments["status"] == "signin":
                self.signin(**arguments)
        except ConnectionRefusedError:
            print("Conneccion negada por el servidor")
        pass

    def login(self, user: str, key: str, **kwargs):
        try:
            self.v4socket.connect((self.host, self.port))
            self.v4socket.send(json.dumps({"status": "login", 'user': user}).encode("utf-8"))
            passwd = QCryptographicHash(sha3_512)
            password = passwd.hash(key.encode("utf-8"), passwd.Sha3_512)
            if __name__ == '__main__':
                with open("test_hash", "wb") as archivo:
                    archivo.write(password)
            self.v4socket.send(len(password).to_bytes(4, byteorder="big"))
            self.v4socket.send(password)
        except ConnectionRefusedError as err:
            print(err)

    def signin(self, user: str, email: str, key: str, **kwargs) -> None:
        self.v4socket.connect((self.host, self.port))
        self.v4socket.send(
            json.dumps({"status": "signin", 'user': user, 'email': email}).encode("utf-8"))
        data = json.loads(self.v4socket.recv(2048).decode("utf-8"))
        if not data["success"]:
            if data["error"] == 1:
                self.v4socket.close()
                message = "User name already exist"
                self.messages.emit({"status": "error", "error": message})
                return print(message)
            elif data["error"] == 2:
                self.v4socket.close()
                message = "Email is already taken"
                self.messages.emit({"status": "error", "error": message})
                return print(message)
            else:
                self.v4socket.close()
                message = "Error n°{}".format(data["error"])
                self.messages.emit({"status": "error", "error": message})
                return print(message)
        else:
            self.messages.emit({"status": "signin", "success": True})
        passwd = QCryptographicHash(sha3_512)
        password = passwd.hash(key.encode("utf-8"), passwd.Sha3_512)
        with open("test_hash", "wb") as archivo:
            archivo.write(password)
            self.v4socket.send(len(password).to_bytes(4, byteorder="big"))
            self.v4socket.send(password)
        self.__init__()


def send_archives(client: socket, file):
    client.send(json.dumps({"status": "file"}).encode('utf-8'))
    with open(file, "rb") as lectura:
        file = lectura.read()

    client.send(len(file).to_bytes(4, byteorder="big"))
    client.send(file)


if __name__ == '__main__':
    c = Client()
    c.signin("esteban", "esteban.faundez@gmail.com", "124567890")
