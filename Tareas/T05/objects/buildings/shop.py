import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QApplication

from objects.template import Objects


class Shop(Objects):
    def __init__(self, x, y):
        super().__init__(pos=(x, y))


class Shopping(QWidget):
    give = pyqtSignal(int)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Shop(1, 2)
    sys.exit(app.exec_())
