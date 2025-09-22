# Importaciones de bibliotecas y/o archivos
from datetime import datetime

# Creaccion de la clase mensaje
class Message:
    def __init__(self, sender: str, receiver: str, subjet: str, body: str):
        self.__sender = sender
        self.__receiver = receiver
        self.__subjet = subjet
        self.__body = body
        self.__date = datetime.now()

    # Creacion de los metodos
    @property
    def sender(self) -> str:
        return self.__sender

    @property
    def receiver(self) -> str:
        return self.__receiver

    @property
    def subjet(self) -> str:
        return self.__subjet

    @property
    def body(self) -> str:
        return self.__body

    @property
    def date(self) -> datetime:
        return self.__date
