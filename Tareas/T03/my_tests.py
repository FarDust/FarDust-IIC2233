import unittest
import modules.basic as basic
from random import choice,randint,random

class ChequearBasics(unittest.TestCase):
    def setUp(self):
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        print(self.numbers_float)
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    def test_asignar_numbers(self):
        self.assertRaises(basic.asignar(choice(self.numbers_float), any))

    def test_asignar_real(self):
        pass
