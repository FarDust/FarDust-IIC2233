def distancia(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** (1 / 2)


def trigonometricas(x1, y1, x2, y2):
    hipotenusa = distancia(x1, y1, x2, y2)
    cos = (x2 - x1) / hipotenusa
    sen = (y2 - y1) / hipotenusa
    return cos, sen