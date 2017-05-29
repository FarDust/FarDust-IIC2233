class MoveMyImageEvent():
    def __init__(self, image, x, y):
        self.image = image
        self.x = x
        self.y = y


def up(unit):
    unit.position = (unit.position[0], unit.position[1] - unit.mov_speed)


def down(unit):
    unit.position = (unit.position[0], unit.position[1] + unit.mov_speed)


def right(unit):
    unit.position = (unit.position[0] + unit.mov_speed, unit.position[1])


def left(unit):
    unit.position = (unit.position[0] - unit.mov_speed, unit.position[1])


def movement_listener(player, keys):
    if 40 in keys:
        down(player)
    elif 38 in keys:
        up(player)
    elif 39 in keys:
        right(player)
    elif 37 in keys:
        left(player)
