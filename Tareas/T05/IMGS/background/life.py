from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QLabel


class HealthBar(QThread):
    def __init__(self):
        super().__init__()
        self.image = QLabel()
        pass

    def run(self):
        while True:
            pass