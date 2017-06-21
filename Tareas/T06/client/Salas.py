import os
import sys
from random import shuffle, choice
from threading import Thread, Timer

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
        if users is not None:
            self.users = users
        if max is not None:
            self.max = max
        if segundos is not None:
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

    def __init__(self, room):
        super().__init__()
        self.room = room
        self.flag = True
        self.setGeometry(150, 150, 400, 500)
        self.setMaximumSize(400, 500)
        self.setMinimumSize(400, 500)
        self.setWindowIcon(QIcon(os.getcwd() + os.sep + "IMGS" + os.sep + "start_icon.png"))
        principal = QVBoxLayout()
        header = QHBoxLayout()
        botones = QVBoxLayout()
        self.getter = Timer(function=self.messages.emit, args=({'status': 'game',
                                                                'option': 'getbuttons',
                                                                'room': self.room},), interval=1)
        self.getter.start()
        self.buttons = [QPushButton("artist", self) for i in range(4)]
        for button in self.buttons:
            botones.addWidget(button, stretch=1)
            button.pressed.connect(self.emit_self)
        self.header = QLabel("Time left:{}".format(20),self)
        header.addWidget(self.header, stretch=1)
        principal.addLayout(header, stretch=6)
        principal.addLayout(botones, stretch=1)
        self.setLayout(principal)

    def emit_self(self):
        button = self.sender()
        if self.room and self.flag:
            self.flag = False
            self.messages.emit({"status": "answer", "room": int(self.room), "content": button.text()})

    def set_buttons(self, buttons: list):
        while len(buttons) < 4:
            buttons.append(choice(buttons))
        shuffle(buttons)
        buttons = buttons[0:4]
        i = 0
        for button in self.buttons:
            button.setText(buttons[i])
            i += 1

    def closeEvent(self, QCloseEvent):
        self.getter.cancel()
        self.messages.emit({"status": "leave"})

    def receiver(self,rules: dict):
        # Poner el cambio de flag y agregar cambios de color
        if rules['status'] == 'answer_match':
            for button in self.buttons:
                if button.text() == rules['ans']:
                    if rules['succes']:
                        button.setObjectName("Correct")
                        self.header.setText("Correcto")
                        self.flag = True
                    else:
                        button.setObjectName("Incorrect")
                        self.flag = True


def console(target):
    while True:
        response = input("hi: ")
        target.addItem(QListWidgetItem(response))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    lista = Room(None)
    lista.show()
    console = Thread(target=console, args=(lista,), daemon=True)
    console.start()
    sys.exit(app.exec_())
