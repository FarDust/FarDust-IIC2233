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
        comandos["evaluar"]("ghdghghg", 1, 60, 2)


class TestPROM(unittest.TestCase):
    def setUp(self):
        self.numbers_float = list(float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = list(x for x in range(0, randint(1, 1000)))

    def test_resultado(self):
        self.assertEqual(comandos["PROM"](self.numbers_int), sum(self.numbers_int) / len(self.numbers_int))

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["PROM"](lambda x: x ** 2, 6, 8, 2, 7)

    def test_referencia_inavalida(self):
        text = interpretar(["PROM", "q"], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["PROM"]()

    @unittest.expectedFailure
    def test_mat_error(self):
        comandos["PROM"]([])

    def test_invalid_comand(self):
        pass


class TestMEDIAN(unittest.TestCase):
    def setUp(self):
        self.numbers_float = list(float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = list(x for x in range(0, randint(1, 1000)))

    def test_resultado(self):
        self.assertEqual(comandos["MEDIAN"](self.numbers_int), comandos["PROM"](
            (self.numbers_int[len(self.numbers_int) // 2 - 1], self.numbers_int[len(self.numbers_int) // 2])) if len(
            self.numbers_int) % 2 == 0 else self.numbers_int[len(self.numbers_int) // 2])
        self.assertEqual(comandos["MEDIAN"](self.numbers_float), comandos["PROM"](
            (self.numbers_float[len(self.numbers_float) // 2 - 1], self.numbers_float[len(self.numbers_float) // 2])) if len(
            self.numbers_float) % 2 == 0 else self.numbers_float[len(self.numbers_float) // 2])

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["MEDIAN"](self.numbers_float,2)

    def test_referencia_inavalida(self):
        text = interpretar(["MEDIAN", "q"], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["MEDIAN"](4)

    def test_mat_error(self):
        pass

    def test_invalid_comand(self):
        pass

class TestVAR(unittest.TestCase):
    def setUp(self):
        self.numbers_float = list(float(x * random()) for x in range(0, randint(1, 1000)))
        self.numbers_int = list(x for x in range(0, randint(1, 1000)))

    def test_resultado(self):
        self.assertEqual(comandos["MEDIAN"](self.numbers_int), comandos["PROM"](
            (self.numbers_int[len(self.numbers_int) // 2 - 1], self.numbers_int[len(self.numbers_int) // 2])) if len(
            self.numbers_int) % 2 == 0 else self.numbers_int[len(self.numbers_int) // 2])
        self.assertEqual(comandos["MEDIAN"](self.numbers_float), comandos["PROM"](
            (self.numbers_float[len(self.numbers_float) // 2 - 1], self.numbers_float[len(self.numbers_float) // 2])) if len(
            self.numbers_float) % 2 == 0 else self.numbers_float[len(self.numbers_float) // 2])

    @unittest.expectedFailure
    def test_argumento_invalido(self):
        comandos["MEDIAN"](self.numbers_float,2)

    def test_referencia_inavalida(self):
        text = interpretar(["MEDIAN", "q"], False)
        if text.find("Causa: Referencia invalida") != -1:
            self.assertEqual(True, False)

    @unittest.expectedFailure
    def test_error_tipo(self):
        comandos["MEDIAN"](4)

    def test_mat_error(self):
        pass

    def test_invalid_comand(self):
        pass


if __name__ == "__main__":
    unittest.main()
