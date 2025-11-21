from typing import List, Dict, Optional
from interfaces.mail_operations import MailOperations
from models.folder import Folder
from models.message import Message

class User(MailOperations):
    """
    Representa un usuario dentro del sistema de correo electrónico.

    Cada usuario posee:
    - una carpeta raíz (Root)
    - una bandeja de entrada (Inbox)
    - una bandeja de enviados (Sent)
    - un árbol de carpetas dinámico
    - filtros automáticos
    - una cola de urgencia
    - un índice rápido de mensajes por asunto

    Requisitos del TP que cumple esta clase:
    ----------------------------------------
    ✔ Gestión completa de carpetas (árbol recursivo)
    ✔ Envío y recepción de mensajes
    ✔ Búsqueda, movimiento y organización de mensajes
    ✔ Filtros automáticos (creación dinámica de carpetas)
    ✔ Integración con BFS mediante el servidor
    ✔ Estructura de datos para prioridad (urgent_queue)

    Esta clase es el núcleo funcional del sistema.
    """

    def __init__(self, name: str):
        self._name = name
        self._root = Folder("Root")
        self._inbox = Folder("Inbox")
        self._sent = Folder("Sent")

        self._root.add_folder(self._inbox)
        self._root.add_folder(self._sent)

        self._filters: Dict[str, str] = {}
        self._urgent_queue: List[Message] = []
        self._message_index: Dict[str, Message] = {}

    # ===================================================================
    # PROPIEDADES
    # ===================================================================
    @property
    def name(self) -> str:
        """Nombre del usuario."""
        return self._name

    @property
    def root(self) -> Folder:
        """Carpeta raíz del usuario."""
        return self._root

    @property
    def inbox(self) -> Folder:
        """Bandeja de entrada."""
        return self._inbox

    @property
    def sent(self) -> Folder:
        """Bandeja de enviados."""
        return self._sent

    # ===================================================================
    # ENVÍO Y RECEPCIÓN DE MENSAJES
    # ===================================================================
    def send(self, server, receiver, subject, body, urgent=False) -> bool:
        """
        Envía un mensaje a través del servidor.

        Pasos:
        1. Se crea un objeto Message.
        2. Se agrega a la carpeta Sent.
        3. Si es urgente, se añade a la cola de urgencia y se ordena con HeapSort.
        4. Se registra en el índice interno.
        5. Se delega al servidor la entrega mediante BFS.

        Retorna True si el mensaje pudo ser entregado.
        """
        msg = Message(self._name, receiver, subject, body, urgent)

        self._sent.add_message(msg)

        if urgent:
            self._urgent_queue.append(msg)
            self._heap_sort_urgent_queue()       # 🔥 ORDENAR CON HEAPSORT
        else:
            self._urgent_queue.append(msg)

        self._message_index[msg.subject] = msg

        return server.send_message(receiver, msg)

    def receive(self, message: Message):
        """
        Recibe un mensaje entrante.

        Si coincide con algún filtro automático, se mueve a la carpeta
        correspondiente. En caso contrario, va a Inbox.
        """
        self._message_index[message.subject] = message

        if not self._apply_filters(message):
            self._inbox.add_message(message)

    # ===================================================================
    # HEAPSORT PARA LA COLA DE URGENCIA
    # ===================================================================
    def _heapify(self, arr: List[Message], n: int, i: int):
        """
        Mantiene la propiedad del heap máximo basado en la fecha del mensaje.
        Los mensajes más recientes tienen mayor prioridad.
        """
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        # Comparar fechas (más nuevo = mayor prioridad)
        if left < n and arr[left].date > arr[largest].date:
            largest = left

        if right < n and arr[right].date > arr[largest].date:
            largest = right

        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)

    def _heap_sort_urgent_queue(self):
        """
        Ordena la cola de urgencia utilizando HeapSort.
        Este algoritmo garantiza que los mensajes más recientes tengan prioridad.
        """
        arr = self._urgent_queue
        n = len(arr)

        # Construcción del heap (heap máximo)
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)

        # Extracción de elementos uno por uno
        for i in range(n - 1, 0, -1):
            arr[i], arr[0] = arr[0], arr[i]  # mover máximo al final
            self._heapify(arr, i, 0)

        # Invertimos porque HeapSort deja el array en orden creciente,
        # y queremos más reciente → primero.
        arr.reverse()

    # ===================================================================
    # FILTROS AUTOMÁTICOS
    # ===================================================================
    def add_filter(self, keyword: str, folder_name: str):
        """Agrega un filtro automático."""
        self._filters[keyword.lower()] = folder_name

    def _apply_filters(self, message: Message) -> bool:
        """Aplica filtros automáticos al mensaje recibido."""
        text = f"{message.subject.lower()} {message.body.lower()}"
        for keyword, folder_name in self._filters.items():
            if keyword in text:
                folder = self.get_folder(folder_name)
                if not folder:
                    folder = Folder(folder_name)
                    self._root.add_folder(folder)
                folder.add_message(message)
                return True
        return False

    # ===================================================================
    # MANEJO DE CARPETAS Y MENSAJES
    # ===================================================================
    def get_folder(self, name: str, folder: Optional[Folder] = None) -> Optional[Folder]:
        """Búsqueda recursiva de carpeta."""
        folder = folder or self._root
        if folder.name.lower() == name.lower():
            return folder
        for sub in folder.subfolders:
            found = self.get_folder(name, sub)
            if found:
                return found
        return None

    def move_message(self, subject: str, target_name: str) -> bool:
        """Mueve un mensaje a otra carpeta."""
        target = self.get_folder(target_name)
        if not target:
            return False
        return self._root.move_message(subject, target)

    def list_inbox(self) -> List[Message]:
        """Retorna la bandeja de entrada."""
        return self._inbox.messages

    def list_filters(self):
        """Lista los filtros activos."""
        return [(k, v) for k, v in self._filters.items()]

    def print_folder_tree(self):
        """Imprime todo el árbol de carpetas."""
        print(f"\nUsuario: {self._name}")
        self._root.print_tree()
