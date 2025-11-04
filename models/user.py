# --- Importaciones de bibliotecas y/o archivos ---
from typing import List, Dict, Optional
from datetime import datetime
from interfaces.mail_operations import MailOperations
from models.folder import Folder
from models.message import Message

# -------------------- Clase User implementando la interfaz --------------------
class User(MailOperations):
    """
    Usuario del sistema de correo.
    Gestiona carpetas, filtros automáticos y cola de prioridad.
    """

    def __init__(self, name: str):
        self._name = name # nombre del usuario
        self._root = Folder("Root") # carpeta raíz
        self._inbox = Folder("Inbox") # carpeta de entrada
        self._sent = Folder("Sent") # carpeta de enviados
        self._root.add_subfolder(self._inbox) # agregar Inbox a Root
        self._root.add_subfolder(self._sent) # agregar Sent a Root

        self._filters: Dict[str, str] = {} # filtros automáticos (keyword -> folder name)
        self._urgent_queue: List[Message] = [] # monticulo de mensajes urgentes
        self._message_index: Dict[str, Message] = {} # índice de mensajes por asunto

    # --- Propiedades ---
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

    # --- Métodos principales ---
    def send_message(self, server, receiver: str, subject: str, body: str, urgent: bool = False):
        msg = Message(self._name, receiver, subject, body, urgent)
        self._sent.add_message(msg)

        if urgent:
            self._urgent_queue.insert(0, msg)

        self._message_index[msg.subject] = msg
        server.deliver_message(receiver, msg)

    def receive_message(self, message: Message):
        self._message_index[message.subject] = message
        if not self._apply_filters(message):
            self._inbox.add_message(message)

    def process_urgent(self):
        while self._urgent_queue:
            msg = self._urgent_queue.pop(0)
            print(f"[URGENTE] Procesando: {msg.subject}")

    # --- Filtros automáticos ---
    def add_filter(self, keyword: str, folder_name: str):
        self._filters[keyword.lower()] = folder_name

    def _apply_filters(self, message: Message) -> bool:
        text = f"{message.subject.lower()} {message.body.lower()}"
        for keyword, folder_name in self._filters.items():
            if keyword in text:
                folder = self.find_folder(folder_name)
                if not folder:
                    folder = Folder(folder_name)
                    self._root.add_subfolder(folder)
                folder.add_message(message)
                return True
        return False

    # --- Búsqueda recursiva ---
    def find_folder(self, name: str, folder: Optional[Folder] = None) -> Optional[Folder]:
        folder = folder or self._root
        if folder.name.lower() == name.lower():
            return folder
        for sub in folder.subfolders:
            found = self.find_folder(name, sub)
            if found:
                return found
        return None

    def move_mail(self, subject: str, target_name: str):
        target = self.find_folder(target_name)
        if not target:
            print("Carpeta destino no encontrada.")
            return False
        if self._root.move_message(subject, target):
            print(f"Mensaje '{subject}' movido a '{target_name}'.")
            return True
        print("Mensaje no encontrado.")
        return False

    # --- Utilidades ---
    def find_message(self, subject: str) -> Optional[Message]:
        return self._message_index.get(subject)

    def list_messages(self) -> List[Message]:
        return self._inbox.messages

    def show_structure(self):
        print(f"\nUsuario: {self._name}")
        self._root.show_tree()
