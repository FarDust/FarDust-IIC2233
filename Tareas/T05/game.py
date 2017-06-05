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
    back = Map(front,600, 600)
    champions = {"hernan": "data/champions/hernan"}
    player = Character(front, 836, 447, "IMGS/units/champions/hernan/individuals/1.png",
                       read_properties(champions["hernan"]))
    c = Nexo(front, 10, 10)
    d = Nexo(front, 1259, 678)
    a = Tower(front, 876, 447, back, "Tower a")
    b = Tower(front, 293, 108, back, "Tower b")
    #e = Tower(front, 836, 447, back)
    back.get_object(a)
    back.get_object(b)
    back.get_object(c)
    #back.get_object(e)
    back.get_player(player, front)
    back.start()
    sys.exit(app.exec_())
