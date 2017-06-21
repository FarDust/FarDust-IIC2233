import os
import sys
import re

from threading import Thread, Timer

import time
from PyQt5.QtCore import QSize, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent, QBitmap
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, \
    QApplication, QSystemTrayIcon, QMessageBox, QLineEdit, QMenuBar, QStatusBar, QMenu, QSlider, QScrollArea, \
    QListWidgetItem, QListView, QListWidget, QLayout

from Salas import Salitas, Sala, Room


def read_styles(path: str, window):
    try:
        with open(path) as styles:
            window.setStyleSheet(styles.read())
    except FileNotFoundError as err:
        print(err)
        print("Error al leer {} , procediendo a usar estilos por defecto".format(path))


class StartMenu(QWidget):
    messages = pyqtSignal(dict)
    success = pyqtSignal()

    def __init__(self, size: int = 60, ratio: tuple = (16, 9), client=None):
        super().__init__()
        self.loggedin = False
        if client:
            self.messages.connect(client.receiver)
        self.flag = True
        self.menu = "start"
        read_styles("styles/master.css", self)
        self.setObjectName("start_menu")
        self.setWindowTitle("Progra Pop")
        self.setWindowIcon(QIcon('IMGS/start_icon.png'))
        main_photo = QPixmap("IMGS/start_menu.png")
        self.main_photo = QLabel("", self)
        self.main_photo.setGeometry(0, 0, ratio[0] * size, ratio[1] * size)
        main_photo = main_photo.scaled(self.main_photo.width(), self.main_photo.height())
        self.main_photo.setPixmap(main_photo)
        self.setGeometry(0, 0, self.main_photo.width(), self.main_photo.height())

        self.button1 = QPushButton("LogIn", self)
        self.button1.setFlat(True)
        self.button1.setIcon(QIcon("IMGS/log_in.png"))
        self.button1.setIconSize(QSize(80, 80))
        self.button1.clicked.connect(self.login)
        self.button1.setObjectName("StartButton")

        self.button2 = QPushButton("SignIn", self)
        self.button2.setFlat(True)
        self.button2.setIcon(QIcon("IMGS/sign_in.png"))
        self.button2.setIconSize(QSize(80, 80))
        self.button2.clicked.connect(self.signin)
        self.button2.setObjectName("StartButton")

        # Template Formulario

        self.name_edit = QLineEdit("user", self)
        self.name_text = QLabel("User: ", self)
        self.name = QHBoxLayout()
        self.name.addWidget(self.name_text)
        self.name.addStretch(1)
        self.name.addWidget(self.name_edit)
        self.name_edit.hide()
        self.name_text.hide()

        self.passwd_edit = QLineEdit("*" * len("password"), self)
        self.passwd_edit.setEchoMode(QLineEdit.Password)
        self.passwd_text = QLabel("Password: ", self)
        self.passwd = QHBoxLayout()
        self.passwd.addWidget(self.passwd_text)
        self.passwd.addStretch(1)
        self.passwd.addWidget(self.passwd_edit)
        self.passwd_edit.hide()
        self.passwd_text.hide()

        self.passwd2_edit = QLineEdit("*" * len("password"), self)
        self.passwd2_edit.setEchoMode(QLineEdit.Password)
        self.passwd2_text = QLabel("Corfim: ", self)
        self.passwd2 = QHBoxLayout()
        self.passwd2.addWidget(self.passwd2_text)
        self.passwd2.addStretch(1)
        self.passwd2.addWidget(self.passwd2_edit)
        self.passwd2_edit.hide()
        self.passwd2_text.hide()

        self.email_edit = QLineEdit("email", self)
        self.email_text = QLabel("Email: ", self)
        self.email = QHBoxLayout()
        self.email.addWidget(self.email_text)
        self.email.addStretch(1)
        self.email.addWidget(self.email_edit)
        self.email_edit.hide()
        self.email_text.hide()

        # Definimos los layout

        self.form = QVBoxLayout()
        self.form.setObjectName("form")
        self.form.addStretch(1)
        self.form.addLayout(self.name)
        self.form.addStretch(1)
        self.form.addLayout(self.passwd)
        self.form.addStretch(1)
        self.form.addLayout(self.passwd2)
        self.form.addStretch(1)
        self.form.addLayout(self.email)
        self.form.addStretch(1)

        self.hbox1 = QHBoxLayout()
        self.hbox1.addStretch(1)
        self.hbox1.addLayout(self.form)
        self.hbox1.addStretch(6)

        self.hbox2 = QHBoxLayout()
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.button1)
        self.hbox2.addStretch(1)
        self.hbox2.addWidget(self.button2)
        self.hbox2.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(3)
        self.vbox.addLayout(self.hbox1)
        self.vbox.addStretch(2)
        self.vbox.addLayout(self.hbox2)
        self.vbox.addStretch(1)
        self.setLayout(self.vbox)

        # Obtenemos tamano de la pantalla principal para centrar la ventana
        screen = QDesktopWidget().screenGeometry()
        main_size = self.geometry()
        self.move((screen.width() - main_size.width()) // 2, (screen.height() - main_size.height()) // 2)
        self.setMaximumSize(main_size.width(), main_size.height())
        self.setMinimumSize(main_size.width(), main_size.height())

    def receiver(self, arguments: dict):
        alert = QMessageBox()
        if self.flag:
            self.flag = False
            if arguments["status"] == "error":
                alert.warning(self, "Server error", "Error: " + arguments["error"], QMessageBox.Ok)
                self.show()
            elif arguments["status"] == 'login':
                if arguments['success']:
                    self.success.emit()
                    self.loggedin = True
                    self.close()
                else:
                    self.login()
                    self.show()
            elif arguments['status'] == 'signin':
                if arguments['success']:
                    self.show()
                    alert.warning(self, "Server says:", "Success: acount created", QMessageBox.Ok)
                    self.home()
                else:
                    self.show()
                    self.signin()
            self.flag = True
            pass
        self.home()
        pass

    def keyPressEvent(self, event: QKeyEvent):
        if (self.menu == "login" or self.menu == "signin") and event.nativeVirtualKey() == 13 and self.flag:  # Enter
            self.send()
            self.home()

    def login(self):
        self.menu = "login"
        self.passwd_text.show()
        self.passwd_edit.show()
        self.passwd2_text.hide()
        self.passwd2_edit.hide()
        self.email_text.hide()
        self.email_edit.hide()
        self.name_edit.show()
        self.name_text.show()

        self.main_photo.setPixmap(
            QPixmap("IMGS/login_menu.jpg").scaled(self.main_photo.width(), self.main_photo.height()))

        self.button1.setIcon(QIcon("IMGS/send.png"))
        self.button1.clicked.connect(self.send)
        self.button1.setText("Log In")

        self.button2.setIcon(QIcon("IMGS/home.png"))
        self.button2.clicked.connect(self.home)
        self.button2.setText("Home")
        pass

    def signin(self):
        self.menu = "signin"
        self.email_text.show()
        self.email_edit.show()
        self.passwd_text.show()
        self.passwd_edit.show()
        self.name_edit.show()
        self.name_text.show()
        self.passwd2_edit.show()
        self.passwd2_text.show()

        self.main_photo.setPixmap(
            QPixmap("IMGS/signin_menu.jpg").scaled(self.main_photo.width(), self.main_photo.height()))

        self.button1.setIcon(QIcon("IMGS/send.png"))
        self.button1.clicked.connect(self.send)
        self.button1.setText("Sign In")

        self.button2.setIcon(QIcon("IMGS/home.png"))
        self.button2.clicked.connect(self.home)
        self.button2.setText("Home")
        pass

    def home(self):
        self.menu = "start"
        self.email_text.hide()
        self.email_edit.hide()
        self.passwd_text.hide()
        self.passwd_edit.hide()
        self.name_edit.hide()
        self.name_text.hide()
        self.passwd2_edit.hide()
        self.passwd2_text.hide()

        self.main_photo.setPixmap(
            QPixmap("IMGS/start_menu.png").scaled(self.main_photo.width(), self.main_photo.height()))

        self.button1.setIcon(QIcon("IMGS/log_in.png"))
        self.button1.clicked.connect(self.login)
        self.button1.setText("Log In")

        self.button2.setIcon(QIcon("IMGS/sign_in.png"))
        self.button2.clicked.connect(self.signin)
        self.button2.setText("Sign In")
        pass

    def send(self):
        sender = {"user": self.name_edit.text(), "key": self.passwd_edit.text()}
        if self.menu == "signin":
            if self.passwd_edit.text() == self.passwd2_edit.text():
                sender.update({"status": "signin", "email": self.email_edit.text()})
                # Send to back
                self.messages.emit(sender)
            else:
                alert = QMessageBox()
                alert.warning(self, "Error", "Las claves no coinciden", QMessageBox.Ok)
                self.signin()
        elif self.menu == "login":
            sender.update({"status": "login"})
            self.messages.emit(sender)

    def close(self):
        if not self.loggedin:
            self.messages.emit({"status": "disconnect"})
        super().close()


class PrograPop(QWidget):
    messages = pyqtSignal(dict)
    internal = pyqtSignal(dict)

    def __init__(self, size=100, menu: QWidget = None, client=None):
        super().__init__()
        self.room = None
        self.lastmessage = dict()
        self.menu = menu
        if not menu:
            self.menu = StartMenu(client=client, size=50)
            self.menu.success.connect(self.show)
        if client:
            self.messages.connect(client.receiver)
        self.setObjectName("PrograPop")
        self.setGeometry(0, 0, 4 * size, 6 * size)
        screen = QDesktopWidget().screenGeometry()
        main_size = self.geometry()
        self.move((screen.width() - main_size.width()) // 2, (screen.height() - main_size.height()) // 2)
        self.setMaximumSize(main_size.width(), main_size.height())
        self.setMinimumSize(main_size.width(), main_size.height())
        self.setWindowIcon(QIcon("IMGS/start_icon.png"))
        self.setWindowTitle("Progra Pop")
        read_styles("styles/master.css", self)

        self.timer = QTimer()
        self.timer.timeout.connect(self.dependencies)
        self.timer.setInterval(1500)

        self.user = QLabel("test text user", self)
        self.user.setObjectName("TextBox")
        self.user.setMaximumSize(130, 37)

        self.points = QLabel("Points: 0", self)
        self.points.setObjectName("Points")
        self.points.setMaximumSize(130, 32)

        status = QHBoxLayout()
        status.addWidget(self.points, stretch=1)
        status.addWidget(self.user, stretch=1)

        games = QVBoxLayout()
        self.games_list = dict()
        self.games = Salitas(self)
        games.addWidget(self.games)

        layout = QVBoxLayout()
        layout.addLayout(status, stretch=1)
        layout.addLayout(games, stretch=1)
        self.setLayout(layout)

        games = Timer(function=self.game_retriever, interval=1)

        console = Thread(target=self.console, daemon=True)
        console.start()

    def show(self):
        if isinstance(self.sender(), StartMenu) and self.menu:
            self.messages.emit({"status": "server_request", "option": "name"})
            super().show()
        elif isinstance(self.menu, StartMenu):
            self.menu.show()
        else:
            super().show()

    def console(self):
        while True:
            response = input("{}$ ".format(os.getcwd())).split(" ")
            if response[0] == "move" and response[1] in self.__dict__.keys() and len(response) == 6 and \
                    isinstance(self.__dict__[response[1]], QWidget):
                self.__dict__[response[1]].move(*[int(i) for i in response[2:]])
            elif response[0] == "help":
                for value in self.__dict__.keys():
                    print(value)
            elif response[0] == "layout":
                pass
            elif response[0] == "show":
                self.show()
            elif response[0] == "hide":
                self.hide()
            elif response[0] == "points":
                self.get_points()

    def games_manager(self, n):
        self.messages.emit({"status": "server_request", "option": "join", "room": n})

    def dependencies(self):
        self.get_points()
        self.game_retriever()

    def game_retriever(self):
        self.messages.emit({"status": "server_request", "option": "rooms"})

    def game_analizer(self):
        games = set(self.games_list.keys())
        self.messages.emit({"status": "server_request", "option": "game_list", "actual_games": games})

    def game_destroyer(self, o: set):
        destroy = set(self.games_list.keys()).difference(o)
        for value in destroy:
            objeto = self.games_list.pop(value)
            self.games.clear()
            del objeto

    def game_format(self, formated: dict):
        if formated['uuid'] in self.games_list:
            current = self.games_list[formated['uuid']]
            current.uptodate(**formated)
        else:
            current = Sala(**formated, target=self.games_manager)
            self.games_list.update({formated['uuid']: current})
            self.games.addItem(current)

    def get_points(self):
        self.messages.emit({"status": "server_request", "option": "points"})

    def set_points(self, points: int):
        self.points.setText("Points : {}".format(points))

    def get_songs(self):
        self.messages.emit({"status": "server_request", "option": "songs"})

    def set_songs(self, songs: dict):
        pass

    def receiver(self, arguments: dict):
        if self.lastmessage != arguments:
            self.lastmessage = arguments
            if not ("option" in arguments.keys() and arguments["option"] == "game_status"):
                # print("Informacion recivida por la interfaz: {}".format(arguments))
                pass
            if arguments["status"] == "server_response" and "option" in arguments.keys():
                if arguments["option"] == "points":
                    self.set_points(arguments["points"])
                elif arguments["option"] == "songs":
                    self.set_songs(arguments["songs"])
                elif arguments["option"] == "name":
                    self.user.setText("User: {}".format(arguments["name"]))
                elif arguments['option'] == 'game_status':
                    self.game_format(arguments['format'])
            elif arguments["status"] == "ready":
                self.timer.start()
                pass
            elif arguments['status'] == 'destroy':
                self.game_destroyer(arguments['compare'])
            elif arguments['status'] == 'disconnect':
                self.menu.loggedin = False
                self.menu.show()
                if self.room:
                    self.room.close()
                self.hide()
            elif arguments['status'] == 'server_display':
                if not self.room:
                    self.room = Room(arguments['room'])
                    read_styles(window=self.room, path=os.getcwd() + os.sep + "styles" + os.sep + "master.css")
                    self.room.title = arguments['room']
                    self.room.setWindowTitle("Sala n° {}".format(arguments['room']))
                    self.internal.connect(self.room.receiver)
                    self.room.messages.connect(self.receiver)
                    self.room.show()
                elif self.room.title == arguments['room'] and 'buttons' in arguments.keys():
                    self.room.set_buttons(arguments['buttons'])
            elif arguments['status'] == 'game':
                if arguments['option'] == 'getbuttons':
                    self.messages.emit(arguments)
            elif arguments['status'] == 'answer':
                self.messages.emit(arguments)
            elif arguments['status'] == 'answer_match':
                self.internal.emit(arguments)
            elif arguments['status'] == 'hide':
                # self.hide()
                pass
            elif arguments['status'] == 'leave':
                self.messages.emit({"status": "leave", "room": self.room.room})
                self.room.destroy(destroyWindow=True)
                self.room = None

    def closeEvent(self, QCloseEvent):
        if self.room:
            self.room.close()
        self.messages.emit({"status": "disconnect"})

    def close(self):
        self.messages.emit({"status": "disconnect"})
        super().close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = PrograPop(menu=1, size=100)
    menu.show()
    sys.exit(app.exec_())
