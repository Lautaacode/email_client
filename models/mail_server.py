# --- Importaciones de bibliotecas y/o archivos ---
from typing import Dict
from models.message import Message
from models.user import User



# -------------------- Clase MailServer --------------------
class MailServer:
    """
    Representa el servidor de correo encargado de registrar usuarios,
    entregar mensajes y mostrar la estructura de carpetas de cada usuario.
    """

    def __init__(self):
        self._users: Dict[str, User] = {}

    # --- Métodos públicos ---
    def register_user(self, name: str):
        """
        Registra un nuevo usuario en el servidor si aún no existe.
        """
        if name not in self._users:
            self._users[name] = User(name)
        else:
            print(f"⚠️ El usuario '{name}' ya está registrado.")

    def deliver_message(self, receiver: str, message: Message):
        """
        Entrega un mensaje al usuario destinatario, si está registrado.
        """
        user = self._users.get(receiver)
        if user:
            user.receive_message(message)
        else:
            print(f"⚠️ El destinatario '{receiver}' no existe en el servidor.")

    def show_structure(self):
        """
        Muestra la estructura de carpetas de todos los usuarios registrados.
        """
        for name, user in self._users.items():
            print(f" Usuario: {name}")
            user.root.show_tree()
            print("-" * 40)

    # --- Propiedad para obtener todos los usuarios (solo lectura) ---
    @property
    def users(self) -> Dict[str, User]:
        return self._users
