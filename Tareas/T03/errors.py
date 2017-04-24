class InvalidArgument(Exception):
    def __init__(self,comando: str) -> None:
        super().__init__("Error de consulta: {}\nCausa: Argumento invalido\n".format(comando))

class InvalidRef(Exception):
    def __init__(self,comando: str) -> None:
        super().__init__("Error de consulta: {}\nCausa: Referencia invalida\n".format(comando))
