# --- Importaciones de bibliotecas y/o archivos ---
from abc import ABC, abstractmethod
from typing import List
from models.message import Message


# -------------------- Interfaz --------------------
class MailOperations(ABC):
    """
    Interfaz que define las operaciones básicas de un cliente de correo electrónico.
    Cualquier clase que la implemente deberá ser capaz de enviar, recibir y listar mensajes.
    """

    # --- Métodos ---
    @abstractmethod
    def send_message(self, server, receiver: str, subject: str, body: str) -> None:
        """Envía un mensaje a través del servidor especificado."""
        pass

    @abstractmethod
    def receive_message(self, message: Message) -> None:
        """Recibe un mensaje entrante."""
        pass

    @abstractmethod
    def list_messages(self) -> List[Message]:
        """Devuelve una lista de mensajes en la bandeja de entrada."""
        pass
