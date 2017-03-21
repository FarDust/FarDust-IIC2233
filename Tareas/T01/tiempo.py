# tiempo v2.1.7
# formato año - mes - dia
# definir 1 como el 1-1-1


class Tiempo:
    def __init__(self):
        pass

    def traducir(self, dias=1):
        fecha = "{}-{}-{}"
        (ano, mes, dia) = (1, 1, 1)
        for _ in range(dias - 1):
            dia += 1
            if mes <= 7:
                if mes == 2:
                    # febrero
                    if ano % 400 == 0 and dia > 29:
                        dia = 1
                        mes += 1
                    elif ano % 4 == 0 and dia > 29 and ano % 100 != 0:
                        dia = 1
                        mes += 1
                    elif dia > 28 and (ano % 4 == 0 and ano % 100 == 0 and ano % 400 != 0):
                        dia = 1
                        mes += 1
                    elif dia > 28 and ano % 4 != 0:
                        dia = 1
                        mes += 1
                elif mes % 2 != 0:
                    # meses 31
                    if dia > 31:
                        dia = 1
                        mes += 1
                elif mes % 2 == 0:
                    # meses 30
                    if dia > 30:
                        dia = 1
                        mes += 1

            elif mes > 7:
                if mes % 2 == 0:
                    # meses 31
                    if dia > 31:
                        dia = 1
                        mes += 1
                elif mes % 2 != 0:
                    # meses 30
                    if dia > 30:
                        dia = 1
                        mes += 1
            if mes == 13:
                mes = 1
                ano += 1
        return fecha.format(ano, str(mes).rjust(2, "0"), str(dia).rjust(2, "0"))

    def re_traducir(self, fecha=""):
        dias = 0
        fecha = fecha.split("-")
        (ano, mes, dia) = (int(fecha[0]), int(fecha[1]), int(fecha[2]))
        dias += dia
        if ano - 1 > -1:
            seculares = (ano - 1) // 100
            bisiestos = ((ano - 1) // 4) - seculares + ((ano - 1) // 400)
            dias += bisiestos * 366
            dias += ((ano - 1) - bisiestos) * 365
        for i in range(mes - 1):
            i += 1
            if i <= 7:
                if (i == 2) and (ano % 4 == 0) and ano % 100 != 0:
                    dias += 29
                elif i == 2 and ano % 400 == 0:
                    dias += 29
                elif i == 2:
                    dias += 28
                elif i % 2 != 0:
                    dias += 31
                else:
                    dias += 30
            else:
                if i % 2 == 0:
                    dias += 31
                else:
                    dias += 30
        return dias

