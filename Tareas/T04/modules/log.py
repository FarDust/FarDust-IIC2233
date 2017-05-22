def header(head: str, path: str):
    try:
        open(path + ".csv", "r", encoding="utf8")
        raise FileExistsError
    except FileNotFoundError:
        with open(path + ".csv", "a", encoding="utf8") as data:
            data.write(head)
    except FileExistsError:
        print("Archivo solicitado ya existe... Ignorando instruccion")
    finally:
        return next(open(path + ".csv", "r", encoding="utf8"))


def log(text: str, path: str, show: bool = False):
    with open(path + ".csv", "a", encoding="utf8") as data:
        data.write(text+"\n")
    if show:
        print(text)
