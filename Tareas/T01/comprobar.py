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
        if inicio > fin or (valor <= fin and valor >= inicio):
            return True

        else:
            print("ERROR: Dato no ingresado correctamente")
            return False
    except:
        return False


def comprobar_fecha(valor):
    valor = str(valor)
    if "-" in valor and len(valor.split("-")) == 3:
        for value in valor.split("-"):
            if not (value.isdigit()):
                return False
            fecha = valor.split("-")
            temp = []
            for i in fecha:
                temp.append(int(i))
            if temp[1] == 2 and temp[2] > 29 and (temp[0]%4 == 0 and temp%100 != 0 or temp[0]%400 == 0):
                return False
            elif temp[1] == 2 and temp[2] > 28 or temp[2] > 31:
                return False
            elif temp[1] > 12:
                return False
            else:
                return True

    else:
        return False
