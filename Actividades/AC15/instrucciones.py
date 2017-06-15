import re


grupo1 = "[^0-9^]*$"
grupo2 = "[^0-9^]+(\.(correcta))[^0-9^]+"
grupo3 = "([A-Za-záéíóú]+\.([A-Za-záéíóú]+)?)+"

def sacar_cafe(text,patron):
    despejar = re.split("[@]",text)
    lista = list()
    for palabra in despejar:
        if bool(re.match(patron,palabra)):
            if bool(re.match("[^0-9^]+(\.(correcta))[^0-9^]+",palabra)):
                lista.append("".join(re.split("\.correcta",palabra)))
            elif "." in palabra:
                palabra = "".join(palabra.split("."))
                lista.append(palabra)
            else:
                lista.append(palabra)
    return " ".join(lista)

with open("AC15.txt","r",encoding="utf-8") as archivito:
    instrucciones = re.split("\n\n",archivito.read())
with open("instrucciones.txt","w",encoding="utf-8") as file:
    file.write(sacar_cafe(instrucciones[0],grupo1)+ "\n+ \n")
    file.write(sacar_cafe(instrucciones[1],grupo2)+ "\n+ \n")
    file.write(sacar_cafe(instrucciones[2],grupo3)+ "\n+ \n")
    
