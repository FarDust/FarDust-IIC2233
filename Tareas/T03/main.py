from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from interprete import interpretar


def id():
    i = 0
    while True:
        yield i
        i += 1


class T03Window(MyWindow):
    consulta = id()

    def __init__(self):
        super().__init__()

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        respuesta = interpretar(querry_array)
        text = "----consulta {}----\n{}\n".format(next(self.consulta), respuesta)
        self.add_answer(text)

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        print(querry_array)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
