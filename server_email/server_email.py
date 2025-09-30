# Importaciones de bibliotecas y/o archivos
from message import Message


# Creaccion de la clase servidor correo
class ServerEmail:
    def __init__(self):
        self.__users = {}

    # Creacion de los metodos
    def register_user(self, user):
        if user.email not in self.__users:
            self.__users[user.email] = user

    def send_message(self, sender, receiver_email, subjet, body):
        if receiver_email in self.__users:
            message = Message(sender.email, receiver_email, subjet, body)
            self.__users[receiver_email].receive_message(message)
        else:
            raise ValueError("Destinatario no registrado en el servidor")

    def list_users(self):
        return list(self.__users.keys())
