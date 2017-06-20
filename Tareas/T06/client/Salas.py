import os
import sys
from random import shuffle
from threading import Thread

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIcon, QStandardItem, QStandardItemModel, QCloseEvent
from PyQt5.QtWidgets import QPushButton, QWidget, QVBoxLayout, QListWidget, QLabel, QApplication, QAction, qApp, \
    QListWidgetItem, QListView, QHBoxLayout


class Sala(QListWidgetItem):
    def __init__(self, uuid: int, users: int, max: int, segundos: int, artist: list, image: QPixmap = None,
                 target=None):
        super().__init__()
        self.segundos = segundos
        self.max = max
        self.users = users
        self.artist = artist
        self.image = image
        self.sala = uuid
        # Lamento esto pero no me dejo usar señales como tal.
        self.signal = target
        self.uptodate()

    def trigger(self):
        self.signal(self.sala)

    def uptodate(self, users: int = None, max: int = None, segundos: int = None, artist: list = None,
                 image: QPixmap = None, **kwargs):
        if users:
            self.users = users
        if max:
            self.max = max
        if segundos:
            self.segundos = segundos
        if artist and isinstance(artist, list):
            self.artist = artist
            shuffle(self.artist)
        while len(self.artist) < 2:
            self.artist.append("")
        if len(self.artist) > 2:
            self.artist = self.artist[0:2]
        self.setText(
            "Users: {}/{} Time left: {}s artits: {}, {}".format(self.users, self.max, self.segundos, *self.artist))
        if image and isinstance(image, QPixmap):
            self.setIcon(QIcon(image))


class Salitas(QListWidget):
    def __init__(self, parent=None, items=list()):
        super().__init__(parent)
        for item in items:
            if isinstance(item, Sala):
                self.addItem(item)
        self.doubleClicked.connect(self.manager)

    def manager(self):
        self.currentItem().trigger()


class Room(QWidget):
    messages = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setGeometry(150, 150, 400, 500)
        self.setMaximumSize(400, 500)
        self.setMinimumSize(400, 500)
        self.setWindowIcon(QIcon(os.getcwd()+os.sep+ "IMGS" +os.sep + "start_icon.png"))
        principal = QVBoxLayout()
        header = QHBoxLayout()
        botones = QVBoxLayout()

        self.buttons = [QPushButton("artist",self) for i in range(4)]
        for button in self.buttons:
            botones.addWidget(button,stretch=1)
        header.addWidget(QLabel("hola",self), stretch=1)
        principal.addLayout(header, stretch=6)
        principal.addLayout(botones,stretch=1)
        self.setLayout(principal)

    def closeEvent(self, QCloseEvent):
        self.messages.emit({"status": "leave"})

    def receiver(self):
        pass



def console(target):
    while True:
        response = input("hi: ")
        target.addItem(QListWidgetItem(response))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lista = GAto()
    lista.show()
    console = Thread(target=console, args=(lista,), daemon=True)
    console.start()
    sys.exit(app.exec_())
