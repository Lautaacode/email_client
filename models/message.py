from datetime import datetime

class Message:
    """
    Representa un mensaje de correo dentro del sistema.

    Cada mensaje contiene:
    - remitente (sender)
    - destinatario (receiver)
    - asunto (subject)
    - cuerpo del mensaje (body)
    - fecha de creación
    - indicador de urgencia (urgent)

    Importancia dentro del TP:
    ✔ Es la unidad fundamental del correo electrónico.
    ✔ Se utiliza en la entrega por BFS (MailServer).
    ✔ Puede ser movido entre carpetas mediante algoritmos recursivos.
    ✔ Soporta prioridad para la cola de urgencia.

    El mensaje está completamente encapsulado y provee métodos para
    su manipulación y representación.
    """

    def __init__(self, sender: str, receiver: str, subject: str, body: str, urgent: bool = False):
        self._sender = sender
        self._receiver = receiver
        self._subject = subject
        self._body = body
        self._date = datetime.now()
        self._urgent = urgent

    # ===================================================================
    # PROPIEDADES
    # ===================================================================
    @property
    def sender(self) -> str:
        """Devuelve el remitente del mensaje."""
        return self._sender

    @property
    def receiver(self) -> str:
        """Devuelve el destinatario del mensaje."""
        return self._receiver

    @property
    def subject(self) -> str:
        """Devuelve el asunto del mensaje."""
        return self._subject

    @property
    def body(self) -> str:
        """Devuelve el cuerpo del mensaje."""
        return self._body

    @property
    def date(self) -> datetime:
        """Devuelve la fecha de creación del mensaje."""
        return self._date

    @property
    def urgent(self) -> bool:
        """Indica si el mensaje es prioritario."""
        return self._urgent
    
    @property
    def urgent(self) -> bool:
        return self._urgent


    # ===================================================================
    # OPERACIONES SOBRE EL MENSAJE
    # ===================================================================
    def toggle_urgent(self):
        """
        Cambia el estado de urgencia del mensaje.

        Esta función mejora el encapsulamiento respecto a modificar
        directamente el atributo privado _urgent.
        """
        self._urgent = not self._urgent

    def is_urgent(self) -> bool:
            """
            Retorna True si el mensaje está marcado como urgente.

            Este método se agrega para compatibilidad con la GUI,
            que utiliza is_urgent() para ordenar y mostrar íconos.
            """
            return self._urgent


    def __str__(self) -> str:
        """
        Devuelve una representación legible del mensaje,
        útil para depuración y listados en consola.
        """
        urgency = " (URGENTE)" if self._urgent else ""
        return (
            f"Asunto: {self._subject}{urgency} | "
            f"De: {self._sender} | Para: {self._receiver} | "
            f"Fecha: {self._date.strftime('%Y-%m-%d %H:%M:%S')}"
        )
