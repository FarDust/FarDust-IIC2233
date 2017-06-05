import sys

from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import QApplication

from map import Map
from window import LeagueOfProgra, StartMenu
from objects.units.champion import Champion, Character
from objects.units.subditos import Minion
from objects.buildings.tower import Tower
from objects.buildings.inhibitor import Inhibitor
from objects.buildings.nexo import Nexo
from scripts.readers import read_properties

if __name__ == '__main__':
    app = QApplication(sys.argv)
    front = LeagueOfProgra(1900, 600)
    app.installEventFilter(front)
    back = Map(600, 600)
    champions = {"hernan": "data/champions/hernan"}
    player = Character(front, 200, 200, "resources/units/champions/hernan/individuals/1.png",
                       read_properties(champions["hernan"]))
    c = Nexo(front, 10, 10)
    a = Tower(front, 876, 447, 200, 10, "Tower a", back, 19)
    b = Tower(front, 90, 90, 200, 10, "Tower b", back, 13)
    back.get_object(a)
    back.get_object(b)
    back.get_object(c)
    back.get_player(player, front)
    back.start()
    sys.exit(app.exec_())
