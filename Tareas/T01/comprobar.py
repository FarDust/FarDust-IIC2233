# Comprobar entrada V1.0.1

def comprobar_int(valor, inicio=1, fin=-1):
    temp = str(valor)
    try:
        valor = int(valor)
        valor + 1
        if (inicio > fin or (valor <= fin and valor >= inicio)):
            return True

        else:
            print("ERROR: Dato no ingresado correctamente")
            return False
    except:
        return False


def comprobar_num(valor, inicio=1, fin=-1):
    temp = str(valor)
    try:
        valor = float(valor)
        valor + 1
        if (inicio > fin or (valor <= fin and valor >= inicio)):
            return True

        else:
            print("ERROR: Dato no ingresado correctamente")
            return False
    except:
        return False
