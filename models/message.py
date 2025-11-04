# --- Importaciones de bibliotecas y/o archivos ---
from datetime import datetime


# -------------------- Clase Message --------------------
class Message:
    """
    Representa un mensaje de correo con asunto, remitente, destinatario y urgencia.
    """

    def __init__(self, sender: str, receiver: str, subject: str, body: str, urgent: bool = False):
        self._sender = sender # remitente
        self._receiver = receiver # destinatario
        self._subject = subject # asunto
        self._body = body # cuerpo del mensaje
        self._date = datetime.now() # fecha de creación
        self._urgent = urgent # indicador de urgencia

    # --- Propiedades ---
    @property
    def sender(self) -> str:
        return self._sender

    @property
    def receiver(self) -> str:
        return self._receiver

    @property
    def subject(self) -> str:
        return self._subject

    @property
    def body(self) -> str:
        return self._body

    @property
    def date(self) -> datetime:
        return self._date

    @property
    def urgent(self) -> bool:
        return self._urgent

    def __str__(self) -> str:
        urgency = " (URGENTE)" if self._urgent else ""
        return (
            f"Asunto: {self._subject}{urgency} | "
            f"De: {self._sender} | Para: {self._receiver} | "
            f"Fecha: {self._date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
