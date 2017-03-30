import unittest
from main import Descifrador

class TestearFormato(unittest.TestCase):

    def setUp(self):
        self.archivo = 'mensaje_marciano.txt'

    def test_archivo(self):
        with open(self.archivo,"r") as texto:
            lineas = texto.readlines()
            text = "".join(lineas).replace('\n', '').replace(" ", "")
            if len(text) != 408:
                return self.assertEqual(len(text), 408)
            for i in text:
                if type(i) != type(""):
                    return self.assertTrue(type(i) != type(""))
            total = 0
            try:
                for numero in text:
                    total += int(numero)
                return self.assertEqual(total, 253)
            except ValueError as err:
                print(err)
                return self.assertTrue(False)


        pass

class TestearMensaje(unittest.TestCase):

    def setUp(self):
        self.descifrador = Descifrador('mensaje_marciano.txt')

    def test_incorrectos(self):
        codigo = self.descifrador.elimina_incorrectos()
        temp = codigo.split(" ")
        for binario in temp:
            if not(6 < len(binario) < 7):
                return self.assertTrue(False)
        return self.assertTrue(True)

    def test_caracteres(self):
        return self.assertFalse("$" in self.descifrador.elimina_incorrectos())

    def test_codificacion(self):
        self.descifrador.lectura_archivo()
        self.descifrador.elimina_incorrectos()
        descifrado = self.descifrador.codigo
        for numero in "".join(descifrado.split(" ")):
            if numero is "0" or numero is "1":
                pass
            else:
                return self.assertTrue(False)
        return self.assertTrue(True)

suite = unittest.TestLoader().loadTestsFromTestCase(TestearFormato)
unittest.TextTestRunner().run(suite)
suite = unittest.TestLoader().loadTestsFromTestCase(TestearMensaje)
unittest.TextTestRunner().run(suite)