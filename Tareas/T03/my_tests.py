import unittest
from interprete import comandos, interpretar, asignar
from random import choice, randint, random


class TestAsignarVariable(unittest.TestCase):
    def setUp(self):
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["asignar"]("x", 1, 2, 3)

    def test_referencia_inavalida(self):
        # No puede tener referencias invalidas este comando
        text = interpretar(["asignar", "x", "y"], False)
        if text.find("Causa:") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["asignar"]([2], [1, 2, 3, 4, 5])

    def test_mat_error(self):
        pass

    @unittest.expectedFailure
    def test_invalid_comand(self):
        text = interpretar(["asignar", "PROM", 2], False)
        if "Causa: Imposible procesar" in text:
            self.assertEqual(True, False)


class TestFiltrar(unittest.TestCase):
    def setUp(self):
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["filtrar"](2, "<", 4, next(self.numbers_float))

    def test_referencia_inavalida(self):
        text = interpretar(["filtrar", "j", "<", 2], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["filtrar"]([next(self.numbers_int, next(self.numbers_float))], "<", "7")

    def test_mat_error(self):
        pass

    @unittest.expectedFailure
    def test_invalid_comand(self):
        text = interpretar(["filtrar", [1, 2, 3, 4], "+", 2], False)
        if "Causa: Imposible procesar" in text:
            self.assertEqual(True, False)


class TestEvaluar(unittest.TestCase):
    def setUp(self):
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["evaluar"](lambda x: x ** 2, 6, 8, 2, 7)

    def test_referencia_inavalida(self):
        text = interpretar(["evaluar", lambda x: x ** 2, 6, "p", 1], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["evaluar"]([next(self.numbers_int, next(self.numbers_float))], "<", "7", 4)

    @unittest.expectedFailure
    def test_mat_error(self):
        comandos["evaluar"](lambda x: 1 / x, -2, 40, 0)

    @unittest.expectedFailure
    def test_invalid_comand(self):
        comandos["evaluar"]("ghdghghg",1,60, 2)

class TestPROM(unittest.TestCase):
    def setUp(self):
        self.numbers_float = (float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = (x for x in range(0, randint(1, 1000)))

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["evaluar"](lambda x: x ** 2, 6, 8, 2, 7)

    def test_referencia_inavalida(self):
        text = interpretar(["evaluar", lambda x: x ** 2, 6, "p", 1], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["evaluar"]([next(self.numbers_int, next(self.numbers_float))], "<", "7", 4)

    @unittest.expectedFailure
    def test_mat_error(self):
        comandos["evaluar"](lambda x: 1 / x, -2, 40, 0)

    @unittest.expectedFailure
    def test_invalid_comand(self):
        comandos["evaluar"]("ghdghghg",1,60, 2)


if __name__ == "__main__":
    unittest.main()
