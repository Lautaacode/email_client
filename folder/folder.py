# Creaccion de la clase carpeta
class Folder:
    def __init__(self, name: str):
        self.__name = name
        self.__messages = []

    # Creacion de los metodos
    @property
    def name(self) -> str:
        return self.__name

    def add_message(self, message):
        self.__messages.append(message)

    def get_messages(self):
        return [msg.subjet for msg in self.__messages]
