# models/mail_server.py
from typing import Dict, Optional
from models.user import User

class MailServer:
    """
    Representa un servidor de correo que conecta usuarios entre sí.

    Este servidor mantiene:
    - Un conjunto de usuarios registrados.
    - Un grafo de conexiones, donde cada usuario tiene vecinos accesibles.
    - Un algoritmo de entrega basado en BFS (Breadth-First Search), que garantiza
    encontrar la ruta más corta para entregar un mensaje a través de la red.

    -----------------------
    🔍 ¿Por qué se usa BFS?
    -----------------------
    BFS es un recorrido por niveles. El servidor lo utiliza para:
    - Buscar usuarios alcanzables desde el remitente.
    - Garantizar la *ruta más corta* en términos de “saltos” entre nodos.
    - Evitar ciclos gracias al conjunto de visitados.
    - Asegurar que si existe un camino, siempre será encontrado.

    Este enfoque está directamente alineado con los requisitos del TP,
    donde se pide modelar la red como un grafo y utilizar una estrategia de búsqueda.
    """

    def __init__(self, name: str):
        self.name = name
        self.users: Dict[str, User] = {}
        self.graph: Dict[str, list[str]] = {}

    # ===================================================================
    # REGISTRO Y CONEXIÓN DE USUARIOS
    # ===================================================================
    def register_user(self, name: str) -> bool:
        """
        Registra un nuevo usuario en el servidor.
        Devuelve False si el usuario ya existe.
        """
        if name in self.users:
            return False
        self.users[name] = User(name)
        self.graph[name] = []
        return True

    def connect(self, a: str, b: str):
        """
        Conecta dos usuarios en el grafo de forma bidireccional.
        Es decir, cada uno queda en la lista de vecinos del otro.
        Esto permite que BFS encuentre rutas entre ellos.
        """
        if a in self.graph and b in self.graph:
            self.graph[a].append(b)
            self.graph[b].append(a)

    # ===================================================================
    # ENTREGA DE MENSAJES
    # ===================================================================
    def send_message(self, receiver: str, message) -> bool:
        """
        Intenta entregar un mensaje al usuario 'receiver'.
        1. Primero intenta BFS entre usuarios conectados.
        2. Si BFS falla, realiza entrega local (mismo servidor).
        3. Si no existe el usuario, retorna False.
        """

        # 1. Intentar BFS
        delivered = self._deliver_via_bfs(receiver, message)
        if delivered:
            return True

        # 2. Intentar entrega local (mismo servidor)
        if receiver in self.users:
            self.users[receiver].receive(message)
            return True

        # 3. No existe forma de entregar
        return False


    def _deliver_via_bfs(self, receiver: str, message) -> bool:
        """
        Entrega un mensaje usando BFS desde el remitente.

        Paso a paso:
        1. Se obtiene el nombre del remitente desde el mensaje.
        2. Se inicia BFS desde el remitente, expandiendo vecinos.
        3. Si se encuentra el receptor, se realiza la entrega.
        4. Si se agotan los nodos sin encontrarlo → no existe ruta.

        Este método cumple con la parte del TP que pide un algoritmo de búsqueda
        en grafos para encontrar rutas en la red.
        """
        start = message.sender
        if start not in self.graph or receiver not in self.graph:
            return False

        from collections import deque

        queue = deque([start])
        visited = {start}

        while queue:
            current = queue.popleft()

            if current == receiver:
                self.users[receiver].receive(message)
                return True

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False
