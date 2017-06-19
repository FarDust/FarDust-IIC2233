import os
import sys
from PyQt5.QtWidgets import QApplication

from local import PrograPop
from connect import Client

PORT = 49500
HOST = None

print(os.curdir)

if __name__ == '__main__':
    cliente = Client(host=HOST, port=PORT)
    app = QApplication(sys.argv)
    menu = PrograPop(size=100, client=cliente)
    cliente.getInteface(menu)
    menu.show()
    sys.exit(app.exec_())
