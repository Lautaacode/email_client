# --- Importaciones de bibliotecas y/o archivos ---
from datetime import datetime


# -------------------- Clase Message --------------------
class Message:
    """
    Representa un mensaje de correo con información del remitente,
    destinatario, asunto, contenido y fecha de envío.
    """

    def __init__(self, sender: str, receiver: str, subject: str, body: str):
        self._sender = sender
        self._receiver = receiver
        self._subject = subject
        self._body = body
        self._date = datetime.now()

    # --- Propiedades encapsuladas ---
    @property
    def sender(self) -> str:
        """Remitente del mensaje."""
        return self._sender

    @property
    def receiver(self) -> str:
        """Destinatario del mensaje."""
        return self._receiver

    @property
    def subject(self) -> str:
        """Asunto del mensaje."""
        return self._subject

    @property
    def body(self) -> str:
        """Contenido del mensaje."""
        return self._body

    @property
    def date(self) -> datetime:
        """Fecha y hora de envío del mensaje."""
        return self._date

    def __str__(self) -> str:
        """Representación legible del mensaje."""
        return (
            f"Asunto: {self._subject} | "
            f"De: {self._sender} | "
            f"Para: {self._receiver} | "
            f"Fecha: {self._date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
