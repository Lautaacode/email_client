# --- Importaciones de bibliotecas y/o archivos ---
from typing import Dict, List
from collections import deque
from models.user import User
from models.message import Message

# -------------------- Clase MailServer --------------------
class MailServer:
    """
    Servidor de correo que administra usuarios y conexiones con otros servidores (grafo).
    """

    def __init__(self, name: str):
        self._name = name # nombre del servidor
        self._users: Dict[str, User] = {} # usuarios registrados
        self._connections: List["MailServer"] = []  # servidores conectados

    @property
    def name(self) -> str:
        return self._name

    @property
    def users(self) -> Dict[str, User]:
        return self._users

    @property
    def connections(self) -> List["MailServer"]:
        return self._connections

    # --- Gestión de usuarios ---
    def register_user(self, name: str):
        if name not in self._users:
            self._users[name] = User(name)
        else:
            print(f"El usuario '{name}' ya está registrado en {self._name}.")

    def deliver_message(self, receiver: str, message: Message):
        user = self._users.get(receiver)
        if user:
            user.receive_message(message)
            print(f"Mensaje entregado a '{receiver}' en {self._name}.")
        else:
            print(f"'{receiver}' no está en {self._name}, buscando en la red...")
            self._bfs_send(receiver, message)

    def show_structure(self):
        print(f"\n=== Servidor: {self._name} ===")
        for user in self._users.values():
            user.show_structure()
        print("-" * 40)

    # --- Red de servidores (grafo) ---
    def connect(self, other_server: "MailServer"):
        if other_server not in self._connections:
            self._connections.append(other_server)
            other_server._connections.append(self)
            print(f"Conectado {self._name} ↔ {other_server.name}")

    def _bfs_send(self, receiver: str, message: Message) -> bool:
        visited = set()
        queue = deque([self])

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.add(current)

            if receiver in current._users:
                current.deliver_message(receiver, message)
                return True

            for neighbor in current._connections:
                if neighbor not in visited:
                    queue.append(neighbor)

        print(f"❌ No se pudo entregar el mensaje a '{receiver}' en la red.")
        return False

    def _dfs_send(self, receiver: str, message: Message, visited=None) -> bool:
        visited = visited or set()
        visited.add(self)

        if receiver in self._users:
            self.deliver_message(receiver, message)
            return True

        for neighbor in self._connections:
            if neighbor not in visited:
                if neighbor._dfs_send(receiver, message, visited):
                    return True
        return False
