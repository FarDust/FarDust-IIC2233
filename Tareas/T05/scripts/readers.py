def read_properties(path: str) -> dict:
    dictionary = dict()
    with open(path+".properties", "r") as arguments:
        for line in arguments:
            temp = line.strip().replace(" ", "").replace("%20", " ").split("=")
            if len(temp) == 2:
                if temp[1].isdigit():
                    temp[1] = int(temp[1])
                dictionary[temp[0]] = temp[1]
    return dictionary

if __name__ == '__main__':
    test_dir = "D:/Users/gabri/Desktop/Programacion Avanzada/FarDust-iic2233-2017-1/Tareas/T05"
    print(read_properties(test_dir +"/data/champions/chau"))