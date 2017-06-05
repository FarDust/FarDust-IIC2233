class MoveMyImageEvent():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


class PlayerKeysSender():
    def __init__(self, cursor: tuple, keys: list):
        self.cursor = cursor
        self.keys = keys


class MoveMyObjectEvent():
    def __init__(self):
        pass


def up(unit):
    unit.position = (unit.position[0], unit.position[1] - unit.mov_speed)


def down(unit):
    unit.position = (unit.position[0], unit.position[1] + unit.mov_speed)


def right(unit):
    unit.position = (unit.position[0] + unit.mov_speed, unit.position[1])


def left(unit):
    unit.position = (unit.position[0] - unit.mov_speed, unit.position[1])


move = {40: down, 38: up, 39: right, 37: left}


def movement_listener(player, keys):
    [move[key](player) for key in keys]
