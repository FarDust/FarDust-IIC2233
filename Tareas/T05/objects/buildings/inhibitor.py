from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QPixmap

from objects.template import Objects


class Inhibitor(QThread, Objects):
    super_minions = pyqtSignal(bool)

    def __init__(self, front, x, y, maxhealth=1000):
        super().__init__(pos=(x, y), maxhealth=maxhealth)
        self.image = QLabel("", front)
        image = QPixmap("resources/buildings/inhibitor.png")
        image = image.scaled(image.width() * 0.6, image.height() * 0.6)
        self.image.setGeometry(x, y, image.width(), image.height())
        self.image.setPixmap(image)
        self.release = True
        self.spawn_event = ReSpawn(self, 60)
        self.start()

    def run(self):
        while True:
            if self.death and self.release:
                self.spawn_event.set()


class ReSpawn(QTimer):
    def __init__(self, parent, seg):
        super().__init__()
        self.parent = parent
        self.setInterval(1000 * seg)
        self.timeout.connect(self.internal_init)
        self.setSingleShot(True)

    def set(self):
        self.parent.release = False
        self.parent.respawn.super_minions.emit(True)
        self.start()

    def internal_init(self):
        self.parent.respawn.super_minions.emit(False)
        self.parent.currenthealth = self.parent.maxhealth
        self.parent.release = True


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication, QWidget, QLabel
    import sys

    app = QApplication(sys.argv)
    a = QWidget()
    a.show()
    b = Inhibitor(a, 10, 10)
    sys.exit(app.exec_())
