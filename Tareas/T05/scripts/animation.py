import sys
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel


class Animation(QLabel):
    def __init__(self, path="", parent=None, framerate=150,**kwargs):
        if parent is None:
            print("No parent, opening a new window...")
            self._auto_init()
        else:
            super().__init__("", parent)
            self.root = path
            with open(self.root+"frames.lop", "r") as archivo:
                self.images = [self.root + i.strip() for i in archivo]
            self.iterator = self._images()
            self.timer = QTimer()
            image = QPixmap(self.images[0])
            self.setPixmap(image)
            self.setGeometry(self.x(), self.y(), image.width(), image.height())
            self.timer.timeout.connect(self.frame)
            self.timer.start(framerate)

    def _auto_init(self):
        from PyQt5.QtWidgets import QApplication, QWidget
        import sys
        app = QApplication(sys.argv)
        window = QWidget()
        window.label = Animation(window, 150)
        window.setGeometry(300, 300, window.label.width(), window.label.height())
        window.show()
        sys.exit(app.exec_())

    def _images(self):
        while True:
            for image in self.images:
                yield image

    def frame(self):
        self.setPixmap(QPixmap(next(self.iterator)))


if __name__ == '__main__':

    label = Animation()
