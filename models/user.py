# --- Importaciones de bibliotecas y/o archivos ---
from typing import List
from interfaces.mail_operations import MailOperations
from models.message import Message
from models.folder import Folder


# -------------------- Clase User implementando la interfaz --------------------
class User(MailOperations):
    """
    Representa a un usuario del sistema de correo.
    Implementa las operaciones definidas por la interfaz MailOperations.
    """

    def __init__(self, name: str):
        self._name = name
        self._root = Folder("Root")
        self._inbox = Folder("Inbox")
        self._sent = Folder("Sent")
        # Se construye la jerarquía de carpetas base
        self._root.add_subfolder(self._inbox)
        self._root.add_subfolder(self._sent)

    # --- Propiedades encapsuladas ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def root(self) -> Folder:
        return self._root

    @property
    def inbox(self) -> Folder:
        return self._inbox

    @property
    def sent(self) -> Folder:
        return self._sent

    # --- Métodos publicos ---
    def send_message(self, server, receiver: str, subject: str, body: str):
        """
        Envía un mensaje a otro usuario a través del servidor.
        Guarda una copia en la carpeta 'Sent'.
        """
        message = Message(self._name, receiver, subject, body)
        self._sent.add_message(message)
        server.deliver_message(receiver, message)

    def find_folder(self, name: str, folder=None):
        """
        Busca recursivamente una carpeta por nombre.
        """
        folder = folder or self._root
        if folder.name == name:
            return folder
        for sub in folder.subfolders:
            res = self._find_folder(name, sub)
            if res:
                return res
        return None

    def move_mail(self, subject: str, folder_name: str):
        """
        Mueve un mensaje desde cualquier carpeta a otra carpeta por nombre.
        """
        target = self._find_folder(folder_name)
        if not target:
            print("Carpeta destino no existe.")
            return

        found = self._root.move_message(subject, target)
        if not found:
            print("Mensaje no encontrado.")

    def receive_message(self, message: Message):
        """Recibe un mensaje y lo guarda en la bandeja de entrada."""
        self._inbox.add_message(message)

    def list_messages(self) -> List[Message]:
        """Lista los mensajes en la bandeja de entrada."""
        return self._inbox.messages
