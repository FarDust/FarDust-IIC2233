from PyQt5.QtCore import QObject
from PyQt5.QtGui import QPixmap, QTransform, QImage
import json

class Animation(QObject):
    def __init__(self, dictionary):
        super().__init__()
        self.dictionary = dictionary
        self.normal = {"up": self.loop("up", "normal"),
                       "down": self.loop("down", "normal"),
                       "right": self.loop("right", "normal"),
                       "left": self.loop("left", "normal"),
                       "ur": self.loop("ur", "normal"),
                       "ul": self.loop("ul", "normal"),
                       "dr": self.loop("dr", "normal"),
                       "dl": self.loop("dl", "normal")}

    def loop(self, key, status):
        while True:
            for pix in self.dictionary[key][status]:
                yield pix


def images(path, *args):
    return ["resources/units/champions/{}/individuals/{}.png".format(path, i) for i in args]


hernan = {
    "idle": None,
    "up": {"normal": images("hernan", 9, 18, 19), "attack": []},
    "down": {"normal": images("hernan", 4, 14, 23), "attack": []},
    "left": {"normal": images("hernan", 1, 6, 11, 16, 21), "attack": []},
    "right": {"normal": images("hernan", 1, 6, 11, 16, 21), "attack": []},
    "ur": {"normal": images("hernan", 0, 7, 17), "attack": []},
    "ul": {"normal": images("hernan", 0, 7, 17), "attack": []},
    "dr": {"normal": images("hernan", 2, 5, 15), "attack": []},
    "dl": {"normal": images("hernan", 2, 5, 15), "attack": []}
}

player = Animation(hernan)
if __name__ == '__main__':
    print(json.dumps(hernan))
