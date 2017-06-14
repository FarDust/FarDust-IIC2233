import re
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

def validate_passwd(s):
    pattern = "[A-Za-z0-9]{16,}"
    return bool(re.match(pattern, s))

class Client(QObject,Thread):
    messages = pyqtSignal(dict)

    def __init__(self, host=HOST, port=PORT):
        super().__init__()
        if host is None:
            host = _LOCALHOST
        self.host = host
        self.port = port
        self.v4socket = socket(family=AF_INET, type=SOCK_STREAM)
        self.v4socket.connect((self.host, self.port))

    def getInteface(self, interface):
        self.messages.connect(interface.receiver)

    def receiver(self, arguments: dict):
        self.getInteface(self.sender())
        rule = arguments['status']
        try:
            if rule == "login":
                self.login(**arguments)
            elif rule == "signin":
                self.signin(**arguments)
            elif rule == 'server_request':
                self.v4socket.send(json.dumps(arguments).encode("utf-8"))

        except ConnectionRefusedError:
            message = "Coneccion negada por el servidor"
            self.messages.emit({"status": "error", "error": message})
            print(message)
        pass

    def server_listener(self):
        while True:
            rules = json.loads(self.v4socket.recv(2048).decode("utf-8"))
            rule = rules['status']
            if rule == 'server_response':
                self.messages.emit(rules)

        pass

    def login(self, user: str, key: str, **kwargs):
        try:
            self.v4socket.send(json.dumps({"status": "login", 'user': user}).encode("utf-8"))
            passwd = QCryptographicHash(sha3_512)
            password = passwd.hash(key.encode("utf-8"), passwd.Sha3_512)
            if __name__ == '__main__':
                with open("test_hash", "wb") as archivo:
                    archivo.write(password)
            self.v4socket.send(len(password).to_bytes(4, byteorder="big"))
            self.v4socket.send(password)
            message = json.loads(self.v4socket.recv(2048).decode("utf-8"))
            if message["status"] == 'login' and message["success"]:
                self.messages.emit({"status": "login", "success": True})
                listener = Thread(target=self.server_listener,name="server_listener",daemon=True)
                listener.start()
            elif message["error"] == 5:
                self.messages.emit({"status":"error", "error":"Wrong user or password"})
            else:
                self.messages.emit({"status": "error", "error": "Error n°{}".format(message["error"])})
        except ConnectionRefusedError:
            self.messages.emit({"status": "error", "error": "Server is dead"})
        except ConnectionResetError:
            self.messages.emit({"status": "error", "error": "Server disconnect you"})
            self.__init__()
        except ConnectionAbortedError:
            self.__init__()

    def signin(self, user: str, email: str, key: str, **kwargs) -> None:
        if not validate_passwd(key):
            message = "Password only recive alphanumeric characters \n and len must be at least 16 characters"
            self.messages.emit({"status": "error", "error": message})
            return print(message)
        self.v4socket.send(
            json.dumps({"status": "signin", 'user': user, 'email': email}).encode("utf-8"))
        data = json.loads(self.v4socket.recv(2048).decode("utf-8"))
        if not data["success"]:
            if data["error"] == 1:
                message = "User name already exist"
                self.messages.emit({"status": "error", "error": message})
                return print(message)
            elif data["error"] == 2:
                message = "Email is already taken"
                self.messages.emit({"status": "error", "error": message})
                return print(message)
            else:
                message = "Error n°{}".format(data["error"])
                self.messages.emit({"status": "error", "error": message})
                return print(message)
        else:
            self.messages.emit({"status": "signin", "success": True})
        passwd = QCryptographicHash(sha3_512)
        password = passwd.hash(key.encode("utf-8"), passwd.Sha3_512)
        self.v4socket.send(len(password).to_bytes(4, byteorder="big"))
        self.v4socket.send(password)


def send_archives(client: socket, file):
    client.send(json.dumps({"status": "file"}).encode('utf-8'))
    with open(file, "rb") as lectura:
        file = lectura.read()

    client.send(len(file).to_bytes(4, byteorder="big"))
    client.send(file)


if __name__ == '__main__':
    c = Client()
    c.signin("esteban", "esteban.faundez@gmail.com", "12345678901234567890")
