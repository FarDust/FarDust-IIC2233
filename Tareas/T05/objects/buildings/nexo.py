from PyQt5.QtCore import pyqtSignal, QThread, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from objects.template import Objects


class Nexo(QThread, Objects):
    finish = pyqtSignal()
    spawn = pyqtSignal()

    def __init__(self, front, x, y, maxhealth=1200):
        super().__init__(pos=(x, y), maxhealth=maxhealth)
        self.image = QLabel("", front)
        image = QPixmap("IMGS/buildings/nexo.png")
        image = image.scaled(image.width() * 0.3, image.height() * 0.3)
        self.image.setGeometry(x, y, image.width(), image.height())
        self.image.setPixmap(image)
        self.spawner = QTimer()
        self.spawner.timeout.connect(self._spawner)
        self.spawner.start(1000)

    def _spawner(self):
        self.spawn.emit()


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
