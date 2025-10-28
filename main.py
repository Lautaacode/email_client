from models.mail_server import MailServer



if __name__ == "__main__":
    server = MailServer()
    server.register_user("alice")
    server.register_user("bob")

    alice = server.users["alice"]
    bob = server.users["bob"]

    alice.send_message(server, "bob", "Hola", "¿Como estas?")
    alice.send_message(server, "bob", "Reunión", "Mañana a las 10am")

    server.show_structure()



    # Buscar mensajes por asunto
    resultados = bob.root.search_by_subject("hola")
    print("\nMensajes con 'hola':")
    for m in resultados:
        print(f"- {m}")
