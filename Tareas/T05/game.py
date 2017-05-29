import sys

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication

from map import Map
from window import LeagueOfProgra, StartMenu
from objects.units.champion import Champion
from objects.units.subditos import Minion
from objects.buildings.tower import Tower



if __name__ == '__main__':
    app = QApplication(sys.argv)
    front = LeagueOfProgra(1900, 600)
    a = Tower(1, 2, 200, 10,"a")
    b = Tower(1, 4, 200, 10,"b")
    back = Map(600, 600)
    back.get_object(a)
    back.get_object(b)
    back.start()
    sys.exit(app.exec_())
