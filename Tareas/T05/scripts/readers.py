def read_properties(path: str) -> dict:
    dictionary = dict()
    with open(path+".properties", "r") as arguments:
        for line in arguments:
            temp = line.strip().replace(" ", "").replace("%20", " ").split("=")
            if len(temp) == 2:
                dictionary[temp[0]] = temp[1]
    return dictionary
