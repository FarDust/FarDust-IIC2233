import os
import json
from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local


def send(value,client: socket):
    client.send(len(value).to_bytes(4, byteorder="big"))
    client.send(value)

def receive():
    # Funcion que recibe cualquier dato mandado por el servidor
    return ""


def get_path(path):
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        return -1
    elif not os.path.isdir(abs_path):
        return 0
    else:
        return abs_path


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.sep.join(C_DIR.split(os.sep) +
                                           path.split(os.sep)))


if __name__ == '__main__':

    HOST = "localhost"
    PORT = 8080
    C_DIR = os.getcwd()
    print("working directory {}".format(C_DIR))

    server_socket = socket(family=AF_INET, type=SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    client = None

    client = None

    while True:
        # Conectarse al servidor
        socket_client, adress = server_socket.accept()
        try:
            socket_client.send(os.getcwd().encode("utf-8"))
            print("Cliente conectado")
            connected = True
            while connected:
                # Recibir comandos
                data = socket_client.recv(2048)
                data_decoded = data.decode('utf-8')
                mensaje = json.loads(data_decoded)
                print("recieved {} from {}:{}".format(mensaje,*adress))
                action = mensaje["status"]
                # message = receive()
                if action == "ls":
                    msg = os.listdir(C_DIR)
                    socket_client.send(json.dumps({"status": "ls", "content": msg}).encode("utf-8"))

                elif action == "logout":
                    connected = mensaje["content"]
                    socket_client.close()
                    print("Cliente desconectado de {}:{}".format(*adress))


                elif action == "get":
                    comandos = mensaje["content"]
                    if len(comandos) == 2:
                        if os.path.isfile(C_DIR + os.sep + comandos[0]):
                            with open(C_DIR + os.sep + comandos[0], "rb") as archivito:
                                archivo = archivito.read()
                            send(client=socket_client, value=archivo)
                        else:
                            if os.path.isdir(C_DIR + os.sep + comandos[0]):
                                socket_client.send("Es una carpeta...")
                            else:
                                socket_client.send("no existe")
                    else:
                        pass

                elif action == "send":
                    comandos = mensaje["content"]
                    if len(comandos) == 2:
                        long_name = int.from_bytes(socket_client.recv(4),byteorder="big")
                        name = socket_client.recv(long_name).decode("utf-8")
                        if not os.path.isfile(C_DIR + os.sep + name):
                            long = int.from_bytes(socket_client.recv(4), byteorder="big")
                            bits = b''
                            while len(bits) < long:
                                bits += socket_client.recv(2048)
                            with open(C_DIR + os.sep + name, "wb") as archivito:
                                archivito.write(bits)
        except ConnectionResetError as err:
            print("Cliente forzo el cierre...")
            connected = False
