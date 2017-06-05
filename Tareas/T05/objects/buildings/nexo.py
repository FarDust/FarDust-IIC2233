from PyQt5.QtCore import pyqtSignal, QThread
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from objects.template import Objects


class Nexo(QThread, Objects):
    finish = pyqtSignal()

    def __init__(self, front, x, y, maxhealth=3000):
        super().__init__(pos=(x, y), maxhealth=maxhealth)
        self.image = QLabel("", front)
        image = QPixmap("resources/buildings/nexo.png")
        image = image.scaled(image.width() * 0.3, image.height() * 0.3)
        self.image.setGeometry(x, y, image.width(), image.height())
        self.image.setPixmap(image)

    def run(self):
        while True:
            if self.death:
                self.finish.emit()


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QWidget
    import sys

    app = QApplication(sys.argv)
    a = QWidget()
    a.show()
    sys.exit(app.exec_())
