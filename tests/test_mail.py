import unittest
from models.mail_server import MailServer , Message


class TestMail(unittest.TestCase):

    def test_send_and_receive(self):
        server = MailServer()
        server.register_user("alice")
        server.register_user("bob")
        alice = server.users["alice"]
        bob = server.users["bob"]

        alice.send_message(server, "bob", "Hola", "Test")
        self.assertEqual(len(bob.inbox.messages), 1)

    def test_search_recursive(self):
        server = MailServer()
        server.register_user("bob")
        bob = server.users["bob"]
        bob.receive_message(Message("alice", "bob", "prueba", "contenido"))

        result = bob.root.search_by_subject("pru")
        self.assertEqual(len(result), 1)


if __name__ == "__main__":
    unittest.main()
