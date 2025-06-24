class EmptyFieldsException(Exception):
    def __init__(self, mensagem="Please don't leave any Field empty! :)"):
        super().__init__(mensagem)