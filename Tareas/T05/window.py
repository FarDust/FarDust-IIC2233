import sys

from PyQt5.QtCore import QThread, QEvent, QPoint, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPixmap, QKeyEvent, QTransform, QImage, QCursor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QDesktopWidget, QLayout, \
    QHBoxLayout, QVBoxLayout, QStyle

from scripts.animation import Animation
from scripts.movement import PlayerKeysSender
from objects.buildings.shop import Shopping


def read_styles(path: str, window):
    try:
        with open(path) as styles:
            window.setStyleSheet(styles.read())
    except FileNotFoundError as err:
        print(err)
        print("Error al leer {} , procediendo a usar estilos por defecto".format(path))


class LeagueOfProgra(QMainWindow):
    movement = pyqtSignal(PlayerKeysSender)
    pause = pyqtSignal(bool)
    life = pyqtSignal()
    ret = pyqtSignal()
    rec = pyqtSignal()
    key_event = pyqtSignal(list)

    def __init__(window, width, height):
        super().__init__()
        read_styles("styles/master.css", window)
        window.setWindowTitle('League of Progra')
        window.setWindowIcon(QIcon('IMGS/main_window_icon.png'))
        window.setGeometry(270, 270, width, height)

        # Inicio de el mapa de fondo
        background_image = QPixmap("IMGS/map.jpg")
        b_size = (background_image.width(), background_image.height())
        window.background = QLabel("", window)
        window.background.move(270, 270)
        window.background.setGeometry(-b_size[0] // 2, -b_size[1] // 2, *b_size)
        window.background.setPixmap(background_image)
        # Cierre del mapa de fondo

        window.setMouseTracking(True)
        window.shop = Shopping()
        window.shop.hide()

        window.start_menu(50)
        window.firstrelease = False
        window.keylist = list()
        window.cheatlist = list()
        window.cursor = (0, 0)

    def start_menu(self, size: int):
        self.menu = StartMenu(self, size)

    @staticmethod
    def actualizar(character):
        label = character.image
        label.move(character.x, character.y)

    def keyPressEvent(self, event):
        self.firstrelease = True
        astr = event.nativeVirtualKey()
        if len(self.cheatlist) < 3:
            self.cheatlist.append(astr)
            print(self.cheatlist)
        else:
            self.cheatlist.pop(0)
            self.cheatlist.append(astr)
        if self.cheatlist == [76, 73,70]: #LIF
            self.life.emit()
        elif self.cheatlist == [82,69,67]: #REC
            self.rec.emit()
        elif self.cheatlist == [82,69,84]: #RET
            self.ret.emit()
        self.keylist.append(astr)

    def keyReleaseEvent(self, event):
        if self.firstrelease:
            self.processmultikeys(self.keylist)

        self.firstrelease = False
        del self.keylist[-1]

    def processmultikeys(self, keyspressed):
        if 67 in keyspressed:
            print(self.cursor)
        if 73 in keyspressed and self.cheatlist[self.cheatlist.index(73)-1] != 76:
            self.start_menu(50)
            self.hide()
        if 80 in keyspressed:
            self.pause.emit(True)
        if 79 in keyspressed:
            if self.shop.isHidden():
                self.shop.show()
            else:
                self.shop.hide()
        self.movement.emit(PlayerKeysSender(self.cursor, keyspressed))


    def eventFilter(self, source, event):
        if event.type() == QEvent.MouseMove:
            cursor = QCursor()
            self.cursor = (cursor.pos().x(), cursor.pos().y())
        return QMainWindow.eventFilter(self, source, event)


class StartMenu(QWidget):
    def __init__(window, main: LeagueOfProgra, size: int = 60):
        super().__init__()
        window.main = main
        read_styles("styles/master.css", window)
        window.setObjectName("start_menu")
        window.setWindowTitle("Bienvenido a League of progra!!!")
        window.setWindowIcon(QIcon('IMGS/main_window_icon.png'))
        window.setGeometry(0, 0, 12 * size, 6 * size)

        # Interfaz (1 Photo + 2 buttons)
        window.main_photo = QLabel("", window)
        window.main_photo.setGeometry((window.width() - 6 * size) // 2, (window.height() - 3 * size) // 3, 6 * size,
                                      3 * size)
        main_photo = QPixmap("IMGS/start_menu.png")
        main_photo.scaled(window.main_photo.width(), window.main_photo.height())
        window.main_photo.setPixmap(main_photo)

        window.new_match_btn = QPushButton("Nuevo juego", window)
        window.new_match_btn.clicked.connect(window.run_main_game)
        window.new_match_btn.setObjectName("default_button")

        window.clear_history_btn = QPushButton("Borrar historial", window)
        window.clear_history_btn.setObjectName("default_button")

        # Definimos los layout
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)
        hbox1.addWidget(window.main_photo)
        hbox1.addStretch(1)

        hbox2 = QHBoxLayout()
        hbox2.addStretch(1)
        hbox2.addWidget(window.new_match_btn)
        hbox2.addStretch(1)
        hbox2.addWidget(window.clear_history_btn)
        hbox2.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addLayout(hbox1)
        vbox.addStretch(2)
        vbox.addLayout(hbox2)
        vbox.addStretch(1)
        window.setLayout(vbox)

        # Obtenemos tamano de la pantalla principal para centrar la ventana
        screen = QDesktopWidget().screenGeometry()
        main_size = window.geometry()
        window.move((screen.width() - main_size.width()) // 2, (screen.height() - main_size.height()) // 2)
        window.setMaximumSize(main_size.width(), main_size.height())

        # Se muestra la ventana
        window.show()

    def run_main_game(self):
        self.main.showFullScreen()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = LeagueOfProgra(1900, 600)
    sys.exit(app.exec_())
