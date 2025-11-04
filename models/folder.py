# --- Importaciones de bibliotecas y/o archivos ---
from __future__ import annotations
from typing import List, Optional
from models.message import Message


# -------------------- Clase Folder --------------------
class Folder:
    """
    Carpeta de correos que puede contener subcarpetas y mensajes.
    Se modela como un árbol general (estructura recursiva).
    """

    def __init__(self, name: str, parent: Optional[Folder] = None):
        self._name = name # nombre de la carpeta
        self._parent = parent # carpeta padre
        self._subfolders: List[Folder] = [] # subcarpetas
        self._messages: List[Message] = [] # mensajes en la carpeta

    # --- Propiedades ---
    @property
    def name(self) -> str:
        return self._name

    @property
    def parent(self) -> Optional[Folder]:
        return self._parent

    @parent.setter
    def parent(self, value: Folder):
        self._parent = value

    @property
    def subfolders(self) -> List[Folder]:
        return self._subfolders

    @property
    def messages(self) -> List[Message]:
        return self._messages

    # --- Métodos ---
    def add_subfolder(self, subfolder: Folder):
        subfolder.parent = self
        self._subfolders.append(subfolder)

    def add_message(self, message: Message):
        self._messages.append(message)

    # --- Búsquedas recursivas ---
    def search_by_subject(self, text: str) -> List[Message]:
        found = [m for m in self._messages if text.lower() in m.subject.lower()]
        for sub in self._subfolders:
            found.extend(sub.search_by_subject(text))
        return found

    def search_by_sender(self, sender: str) -> List[Message]:
        found = [m for m in self._messages if m.sender == sender]
        for sub in self._subfolders:
            found.extend(sub.search_by_sender(sender))
        return found

    def move_message(self, subject: str, target_folder: "Folder") -> bool:
        for m in self._messages:
            if m.subject == subject:
                self._messages.remove(m)
                target_folder.add_message(m)
                return True
        for sub in self._subfolders:
            if sub.move_message(subject, target_folder):
                return True
        return False

    def show_tree(self, level: int = 0):
        print("  " * level + f"📁 {self._name} ({len(self._messages)} mensajes)")
        for sub in self._subfolders:
            sub.show_tree(level + 1)
