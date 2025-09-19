# Creaccion de la clase mensaje
class Message:
    def __init__(self, sender, receiver, subjet, body):
        self.__sender
        self.__receiver
        self.__subjet
        self.__body

    # creacion de los metodos getters / setters

    @property
    def sender(self):
        return self.__sender

    @sender.setter
    def sender(self, new_sender):
        self.__sender = new_sender

    @property
    def receiver(self):
        return self.__receiver

    @receiver.setter
    def receiver(self, new_receiver):
        self.__receiver = new_receiver

    @property
    def subjet(self):
        return self.__subjet

    @subjet.setter
    def subjetl(self, new_subjet):
        self.__subjet = new_subjet

    @property
    def body(self):
        return self.__body

    @body.setter
    def body(self, new_body):
        self.__body = new_body
