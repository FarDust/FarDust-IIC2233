class Objects():
    def __init__(self, pos: tuple, maxhealth: int = 0):
        self.pos = pos
        self.maxhealth = maxhealth
        self.inmune = False
        if self.maxhealth == 0:
            self.inmune = True
        self.currenthealth = maxhealth