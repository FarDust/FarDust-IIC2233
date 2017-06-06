import sys
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QHBoxLayout, QVBoxLayout, QPushButton

from objects.template import Objects


class Shop(Objects):
    def __init__(self, x, y):
        super().__init__(pos=(x, y))


class Shopping(QWidget):
    give = pyqtSignal(int, str)

    def __init__(self):
        super().__init__()

        self.setWindowIcon(QIcon('IMGS/main_window_icon.png'))
        self.setWindowTitle("Tienda")

        self.armamano = QPushButton("Arma de mano", self)
        self.armamano.clicked.connect(self.arma_mano)
        self.armamano.setObjectName("default_button")
        icon = QIcon()
        icon.addPixmap(QPixmap("IMGS/icons/shop/inactive/Weapon_01_Inactive.png"))
        self.armamano.setIcon(icon)

        self.armadistancia = QPushButton("Arma Distancia", self)
        self.armamano.clicked.connect(self.arma_distancia)
        self.armadistancia.setObjectName("default_button")
        icon = QIcon()
        icon.addPixmap(QPixmap("IMGS/icons/shop/inactive/Weapon_17_Inactive.png"))
        self.armadistancia.setIcon(icon)

        self.botas = QPushButton("Botas", self)
        self.botas.clicked.connect(self.botitas)
        self.botas.setObjectName("default_button")
        icon = QIcon()
        icon.addPixmap(QPixmap("IMGS/icons/shop/inactive/Weapon_13_Inactive.png"))
        self.botas.setIcon(icon)

        self.baculo = QPushButton("Baculo", self)
        self.baculo.clicked.connect(self.baculos)
        self.baculo.setObjectName("default_button")
        icon = QIcon()
        icon.addPixmap(QPixmap("IMGS/icons/shop/inactive/Weapon_20_Inactive.png"))
        self.baculo.setIcon(icon)

        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(self.armamano)
        hbox1.addStretch(1)
        hbox1.addWidget(self.armadistancia)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(self.botas)
        hbox2.addStretch(1)
        hbox2.addWidget(self.baculo)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addStretch(2)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        self.setLayout(vbox)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.nativeVirtualKey() == 79:
            self.hide()

    def arma_mano(self):
        self.give.emit(2, "basic_atk")

    def arma_distancia(self):
        self.give.emit(2, "atk_range")

    def botitas(self):
        self.give.emit(2, "mov_speed")

    def baculos(self):
        self.give.emit(2, "")

    def armor(self):
        self.give.emit(2, "maxhealth")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    a = Shopping()
    a.show()
    sys.exit(app.exec_())
