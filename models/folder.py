# Creaccion de la clase usuario
class User:
    def __init__(self, name, password, email):
        self.__name = name
        self.__password = password
        self.__email = email

    # creacion de los metodos getters / setters

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name ):
        self.__name = new_name

    @property
    def password(self):
        return self.__password

    @name.setter
    def password(self, new_password):
        self.__password = new_password

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        self.__email = new_email
