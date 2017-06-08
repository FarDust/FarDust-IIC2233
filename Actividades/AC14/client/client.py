import os

from socket import socket, AF_INET, AF_INET6, SOCK_STREAM, _LOCALHOST, _LOCALHOST_V6
from threading import Thread, Timer, Event, Barrier, Lock, Condition, local
import json

def send(name,value,server: socket):
    nombre = name.encode("utf-8")
    server.send(len(nombre).to_bytes(4,byteorder="big"))
    server.send(nombre)
    server.send(len(value).to_bytes(4, byteorder="big"))
    server.send(value)


def receive(server_socket):
    # Funcion que recibe cualquier dato mandado por el servidor
    data = server_socket.recv(2048)
    data_decoded = data.decode('utf-8')
    mensaje = json.loads(data_decoded)
    return mensaje


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

    C_DIR = os.getcwd()
    HOST = "localhost"
    PORT = 8080

    server_socket = socket(family=AF_INET, type=SOCK_STREAM)

    try:
        server_socket.connect((HOST, PORT))
        print("connected to server")
    except Exception as err:
        print(err)
    #finally:
    #    server_socket.close()

    S_DIR = server_socket.recv(2048).decode("utf-8")
    connected = True
    while connected:
        command = input(S_DIR + " $ ")
        commands = command.split(" ")

        if commands[0] == "logout":
            # Aviso al servidor que me desconecto
            print("Disconecting...")
            server_socket.send(json.dumps({"status": "logout", "content": False}).encode("utf-8"))
            connected = False
            server_socket.close()

        elif commands[0] == "ls":
            msj_final = {'status': 'ls'}
            msj_final_json = json.dumps(msj_final)
            server_socket.send(msj_final_json.encode('utf-8'))
            message = receive(server_socket)
            for i in message["content"]:
                print(i)
            # Muetra carpetas y archivos en el directorio del servidor
            pass


        elif commands[0] == "get":
            # Le pides un archivo al servidor
            server_socket.send(json.dumps({"status": "get", "content": commands[1:]}).encode('utf-8'))
            long = int.from_bytes(server_socket.recv(4), byteorder="big")
            bits = b''
            while len(bits) < long:
                bits += server_socket.recv(2048)
            with open(C_DIR + os.sep + commands[2], "wb") as archivito:
                archivito.write(bits)

        elif commands[0] == "send":
            # le mandas un archivo al servidor
            file_path = get_abs_path(commands[1])
            if os.path.exists(file_path):
                server_socket.send(json.dumps({"status": "send", "content": commands[1:]}).encode('utf-8'))
                with open(file_path,"rb") as archivito:
                    file = archivito.read()
                send(commands[2],file,server_socket)

            else:
                print(commands[1] + " doesn't exist.")
        commands.clear()