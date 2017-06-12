import sys
from PyQt5.QtWidgets import QApplication

from client.local import StartMenu
from client.connect import Client

PORT = 49500
HOST = None

if __name__ == '__main__':
    cliente = Client(host=HOST, port=PORT)
    app = QApplication(sys.argv)
    menu = StartMenu(size=50, client=cliente)
    cliente.getInteface(menu)
    menu.show()
    sys.exit(app.exec_())
