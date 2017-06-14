import sys
from PyQt5.QtWidgets import QApplication

from client.local import PrograPop
from client.connect import Client

PORT = 49500
HOST = None

if __name__ == '__main__':
    cliente = Client(host=HOST, port=PORT)
    app = QApplication(sys.argv)
    menu = PrograPop(size=100, client=cliente)
    cliente.getInteface(menu)
    menu.show()
    sys.exit(app.exec_())
