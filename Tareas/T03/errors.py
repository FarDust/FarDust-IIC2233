class InvalidArgument(Exception):
    def __init__(self, mesaje=""):
        super().__init__(mesaje)


class InvalidRef(Exception):
    def __init__(self, mesaje="") -> None:
        super().__init__(mesaje)


class InvalidCommand(Exception):
    def __init__(self, mesaje="") -> None:
        super().__init__(mesaje)
