# Importaciones de bibliotecas y/o archivos
from user import User
from server_email import ServerEmail

# Creaccion de la clase main
def main():
    # Crear servidor
    server = ServerEmail()
    # Crear array de usuarios
    users = []
    # Crear usuarios
    alice = User("Alice", "alice@mail.com")
    users.append(alice)
    bob = User("Bob", "bob@mail.com")
    users.append(bob)

    # Registrar usuarios
    server.register_user(alice)
    server.register_user(bob)

    # Enviar mensaje
    server.send_message(alice, "bob@mail.com", "Hola Bob", "¿Cómo estás?")
    server.send_message(alice, "bob@mail.com", "Hola Bob", "¿Cómo estás?")
    server.send_message(bob, "alice@mail.com", "Hola Bob", "¿Cómo estás?")

    # Lista mensajes de usuarios
    for user in users:
        print(f"Mensajes de {user.name}:", user.get_messages())


if __name__ == "__main__":
    main()
