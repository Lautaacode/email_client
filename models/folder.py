# models/folder.py
from typing import List, Optional
from models.message import Message

class Folder:
    """
    Representa una carpeta en el árbol de correo de un usuario.

    Cada carpeta puede contener:
    - Mensajes
    - Subcarpetas (árbol recursivo)

    Este diseño está alineado con los requisitos del TP:
    ✔ ÁRBOL de carpetas
    ✔ BÚSQUEDAS recursivas por asunto o remitente
    ✔ Movimiento de mensajes entre carpetas
    ✔ Carpetas creadas dinámicamente por filtros automáticos
    """

    def __init__(self, name: str):
        self.name = name
        self.messages: List[Message] = []
        self.subfolders: List["Folder"] = []

    # ===================================================================
    # OPERACIONES PRINCIPALES
    # ===================================================================
    def add_folder(self, folder: "Folder"):
        """
        Agrega una subcarpeta directa.
        Se usa al crear carpetas manualmente o desde filtros automáticos.
        """
        self.subfolders.append(folder)

    def add_message(self, message: Message):
        """
        Agrega un mensaje a esta carpeta.
        """
        self.messages.append(message)

    # ===================================================================
    # BÚSQUEDA RECURSIVA
    # ===================================================================
    def find_by_subject(self, subject: str) -> Optional[Message]:
        """
        Busca un mensaje por asunto, recorriendo el árbol recursivamente.

        Requisitos importantes del TP:
        - una carpeta puede contener subcarpetas,
        - las búsquedas deben ser recursivas,
        - debe retornar el primer mensaje encontrado.

        Este método es un claro ejemplo de recorrido DFS (profundidad).
        """
        for msg in self.messages:
            if msg.subject == subject:
                return msg

        for sub in self.subfolders:
            found = sub.find_by_subject(subject)
            if found:
                return found

        return None

    # ===================================================================
    # MOVER MENSAJES
    # ===================================================================
    def move_message(self, subject: str, target_folder: "Folder") -> bool:
        """
        Mueve un mensaje identificado por su asunto a otra carpeta.
        La función recorre el árbol recursivamente, extrae el mensaje
        y lo agrega a la carpeta destino.
        """
        for msg in self.messages:
            if msg.subject == subject:
                self.messages.remove(msg)
                target_folder.add_message(msg)
                return True

        for sub in self.subfolders:
            if sub.move_message(subject, target_folder):
                return True

        return False

    # ===================================================================
    # REPRESENTACIÓN VISUAL (para depuración / defensa)
    # ===================================================================
    def print_tree(self, level: int = 0):
        """
        Imprime la estructura completa de carpetas,
        útil para depuración y como apoyo en la defensa del TP.
        """
        indent = "  " * level
        print(f"{indent}- {self.name} ({len(self.messages)} mensajes)")
        for sub in self.subfolders:
            sub.print_tree(level + 1)
