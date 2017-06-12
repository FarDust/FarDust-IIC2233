import sys

from PyQt5.QtCore import QSize, pyqtSignal
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QDesktopWidget, \
    QApplication, QSystemTrayIcon, QMessageBox, QLineEdit


def read_styles(path: str, window):
    try:
        with open(path) as styles:
            window.setStyleSheet(styles.read())
    except FileNotFoundError as err:
        print(err)
        print("Error al leer {} , procediendo a usar estilos por defecto".format(path))


class StartMenu(QWidget):
    messages = pyqtSignal(dict)

    def __init__(self, main: QMainWindow = None, size: int = 60, ratio: tuple = (16, 9), client=None):
        super().__init__()
        if client:
            self.messages.connect(client.receiver)
        self.main = main
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
        self.passwd_text = QLabel("Password: ", self)
        self.passwd = QHBoxLayout()
        self.passwd.addWidget(self.passwd_text)
        self.passwd.addStretch(1)
        self.passwd.addWidget(self.passwd_edit)
        self.passwd_edit.hide()
        self.passwd_text.hide()

        self.passwd2_edit = QLineEdit("*" * len("password"), self)
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
        self.flag = False
        if self.flag:
            if arguments["status"] == "error":
                alert.warning(self, "Server says:", "Error: " + arguments["error"], QMessageBox.Ok)
            elif arguments['status'] == 'signin':
                if arguments['success']:
                    self.show()
                    alert.warning(self, "Server says:", "Success: acount created", QMessageBox.Ok)
                    self.login()
            self.flag = True
            pass
        pass

    def keyPressEvent(self, event: QKeyEvent):
        print("key: ", event.nativeVirtualKey())
        if (self.menu == "login" or self.menu == "signin") and event.nativeVirtualKey() == 13 and self.flag:  # Enter
            self.send()

    def login(self):
        self.menu = "login"
        self.passwd_text.show()
        self.passwd_edit.show()
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
                self.hide()
            else:
                alert = QMessageBox()
                alert.warning(self, "Error", "Las claves no coinciden", QMessageBox.Ok)
                self.signin()
        elif self.menu == "login":
            sender.update({"status": "login"})
            self.messages.emit(sender)
            self.hide()


class PrograPop(QMainWindow):
    messages = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        self.setObjectName("PrograPop")
        

    def reciever(self,arguments:dict):
        pass



class Carga(QMessageBox):
    def __init__(self):
        super().__init__()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    menu = StartMenu(size=50)
    menu.show()
    sys.exit(app.exec_())
