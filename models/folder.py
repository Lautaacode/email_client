# --- Importaciones de bibliotecas y/o archivos ---
from __future__ import annotations
from typing import List, Optional
from models.message import Message


# -------------------- Clase Folder --------------------
class Folder:
    """
    Representa una carpeta que puede contener subcarpetas y mensajes.
    Forma parte de una estructura recursiva (árbol general).
    """

    def __init__(self, name: str, parent: Optional[Folder] = None):
        self._name = name
        self._parent = parent
        self._subfolders: List[Folder] = []
        self._messages: List[Message] = []

    # --- Propiedades encapsuladas ---
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

    # --- Métodos públicos ---

    # --- Estructura recursiva ---
    def add_subfolder(self, subfolder: Folder):
        """Agrega una subcarpeta a la carpeta actual."""
        subfolder.parent = self
        self._subfolders.append(subfolder)

    def add_message(self, message: Message):
        """Agrega un mensaje a la carpeta actual."""
        self._messages.append(message)

    # --- Búsqueda recursiva ---
    def search_by_subject(self, text: str) -> List[Message]:
        """
        Busca mensajes por texto contenido en el asunto.
        Complejidad temporal: O(n) siendo n la cantidad total de mensajes en el árbol.
        """
        found = [m for m in self._messages if text.lower() in m.subject.lower()]
        for sub in self._subfolders:
            found.extend(sub.search_by_subject(text))
        return found

    def search_by_sender(self, sender: str) -> List[Message]:
        """Busca mensajes por nombre del remitente (recursivo)."""
        found = [m for m in self._messages if m.sender == sender]
        for sub in self._subfolders:
            found.extend(sub.search_by_sender(sender))
        return found

    # --- Representación visual del árbol ---
    def show_tree(self, level: int = 0):
        """Muestra la estructura jerárquica de carpetas y cantidad de mensajes."""
        print("  " * level + f" {self._name} ({len(self._messages)} mensajes)")
        for sub in self._subfolders:
            sub.show_tree(level + 1)
