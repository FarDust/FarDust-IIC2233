from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from interprete import interpretar


def id():
    i = 1
    while True:
        yield i
        i += 1


class T03Window(MyWindow):
    consulta = id()

    def __init__(self):
        super().__init__()

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        try:
            respuestas = [interpretar([consulta], graph=True)[0] for consulta in querry_array]
            [self.add_answer("----Consulta {}----\n{}\n".format(next(self.consulta), respuesta)) for respuesta in
             respuestas]
        # Solo por razones de debug para que la ventana no caiga.
        except Exception as err:
            print(err)

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        try:
            respuestas = interpretar(querry_array, False)
            with open("resultados.txt", "w") as archivo:
                [archivo.write("----Consulta {}----\n{}\n".format(next(self.consulta), respuesta)) for respuesta
                 in respuestas]
                archivo.close()
        # Solo por razones de debug para que la ventana no caiga.
        except Exception as err:
            print(err)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
