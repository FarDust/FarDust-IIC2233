from PyQt5.QtCore import QThread

class IA(QThread):
    def __init__(self, personalidad):
        super().__init__()
        self.personalidad = personalidad
        self.start()

    def run(self):
        self.personalidad(self)
        pass