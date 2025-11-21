from abc import ABC, abstractmethod
from typing import List
from models.message import Message

class MailOperations(ABC):
    """
    Interfaz que define las operaciones mínimas de un cliente de correo.

    Esta clase abstracta asegura el cumplimiento de:
    ✔ Abstracción
    ✔ Polimorfismo
    ✔ Programación Orientada a Interfaces (requisito del TP)

    Cualquier clase que represente un usuario deberá implementar:
    - send(): envío de mensajes a través del servidor.
    - receive(): recepción y clasificación del mensaje.
    - list_inbox(): listado de mensajes de la bandeja principal.
    """

    # ===================================================================
    # MÉTODOS ABSTRACTOS
    # ===================================================================
    @abstractmethod
    def send(self, server, receiver: str, subject: str, body: str) -> None:
        """
        Envia un mensaje utilizando el servidor especificado.
        Debe crear un objeto Message y delegar su entrega al servidor.
        """
        pass

    @abstractmethod
    def receive(self, message: Message) -> None:
        """
        Procesa un mensaje recibido.
        Puede involucrar filtros automáticos o bandejas especiales.
        """
        pass

    @abstractmethod
    def list_inbox(self) -> List[Message]:
        """
        Retorna la lista de mensajes contenidos en la bandeja de entrada.
        """
        pass
