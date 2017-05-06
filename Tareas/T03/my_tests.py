import unittest
from interprete import comandos
from random import choice,randint,random

class AsignarVariable(unittest.TestCase):
    def setUp(self):
        self.var = comandos["asignar"]
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    def test_argumento_invalido(self):
        
        pass



    def test_asignar_real(self):
        pass
