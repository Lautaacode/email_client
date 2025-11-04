import unittest
from models.mail_server import MailServer
from models.message import Message


class TestMailSystem(unittest.TestCase):

    def setUp(self):
        self.serverA = MailServer("ServerA")  # servidor de origen
        self.serverB = MailServer("ServerB")  # servidor intermedio
        self.serverC = MailServer("ServerC")  # servidor de destino

        self.serverA.connect(self.serverB)  # conectar A con B
        self.serverB.connect(self.serverC)  # conectar B con C

        self.serverA.register_user("alice")  # registrar usuario Alice en A
        self.serverC.register_user("bob")  # registrar usuario Bob en C

        self.alice = self.serverA.users["alice"]  # obtener instancia de Alice
        self.bob = self.serverC.users["bob"]  # obtener instancia de Bob

    def test_send_and_receive_message(self):
        # Alice envía mensaje a Bob
        self.alice.send_message(self.serverA, "bob", "Hola", "¿Cómo estás?")
        # obtener mensajes en la bandeja de entrada de Bob
        inbox = self.bob.list_messages()
        self.assertEqual(len(inbox), 1)  # verificar que Bob recibió el mensaje
        # verificar asunto del mensaje
        self.assertEqual(inbox[0].subject, "Hola")

    def test_filters(self):
        # Bob agrega filtro para "reunión"
        self.bob.add_filter("reunión", "Meetings")
        # Alice envía mensaje con asunto "Reunión"
        self.alice.send_message(self.serverA, "bob", "Reunión", "Mañana")
        meetings = self.bob.find_folder(
            "Meetings")  # buscar carpeta "Meetings"
        self.assertIsNotNone(meetings)  # verificar que la carpeta existe
        # verificar que el mensaje fue filtrado correctamente
        self.assertEqual(len(meetings.messages), 1)

    def test_urgent_queue(self):
        self.alice.send_message(self.serverA, "bob", "Normal", "Mensaje común")  # mensaje normal
        self.alice.send_message(self.serverA, "bob", "Urgente", "Mensaje urgente", urgent=True) # mensaje urgente
        self.assertEqual(len(self.alice._urgent_queue), 1) # verificar cola urgente
        self.alice.process_urgent() # procesar mensajes urgentes
        self.assertEqual(len(self.alice._urgent_queue), 0) # verificar cola vacía

    def test_network_bfs_and_dfs(self):
        msg1 = Message("alice", "bob", "Via BFS", "Mensaje BFS") # mensaje para BFS
        msg2 = Message("alice", "bob", "Via DFS", "Mensaje DFS") # mensaje para DFS
        self.assertTrue(self.serverA._bfs_send("bob", msg1)) # probar envío BFS
        self.assertTrue(self.serverA._dfs_send("bob", msg2)) # probar envío DFS


if __name__ == "__main__":
    unittest.main()
