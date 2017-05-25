class Spell:
    def __init__(self,name, efect, cooldown: int = 0):
        self.name = name
        self.efect = efect
        self.cooldown = cooldown

    def launch(self):
        self.efect()

def alto_ahi():
    pass

spells = {
    "alto ahi!!!": alto_ahi




}

