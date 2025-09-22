# Creaccion de la clase usuario
class User:
    def __init__(self, name: str, email: str):
        self.__name = name
        self.__email = email
        self.__inbox = []

    # Creacion de metodos
    @property
    def name(self) -> str:
        return self.__name

    @property
    def email(self) -> str:
        return self.__email

    def receive_message(self, message):
        self.__inbox.append(message)

    def list_messages(self):
        return [msg.subjet for msg in self.__inbox]
