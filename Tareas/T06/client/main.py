import json
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
import sys
from uuid import getnode, uuid4

from PyQt5.QtCore import QCryptographicHash

socket1 = socket(family=AF_INET, type=SOCK_STREAM)
socket2 = socket(family=AF_INET6, type=SOCK_STREAM)

sha512 = 6
sha3_512 = 10

PORT = 49500
HOST = _LOCALHOST


def send_archives(client: socket, file):
    client.send(json.dumps({"status": "file"}).encode('utf-8'))
    with open(file, "rb") as lectura:
        file = lectura.read()

    client.send(len(file).to_bytes(4, byteorder="big"))
    client.send(file)

if __name__ == '__main__':
    socket1.connect((HOST, PORT))
    socket1.send(json.dumps({"status": "login", 'user': 'gabriel'}).encode("utf-8"))
    passwd = QCryptographicHash(sha3_512)
    password = passwd.hash("1234567890".encode("utf-8"), passwd.Sha3_512)
    with open("test_hash", "wb") as archivo:
        archivo.write(password)
    socket1.send(len(password).to_bytes(4, byteorder="big"))
    socket1.send(password)
    socket1.close()
