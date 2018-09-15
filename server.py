"""Maths server.

Usage:
$ python server.py [address=$MATHS_SERVER_ADDRESS|localhost:4042]
"""

import select
import socket
from dataclasses import dataclass

from address import to_address, from_argv
from simpleeval import InvalidExpression, simple_eval


def evaluate(expression: str) -> str:
    """Evaluate an expression and return a response message."""
    try:
        return str(simple_eval(expression))
    except InvalidExpression as e:
        return f'Invalid expression: {e}'
    except SyntaxError as e:
        return f'Syntax error: {e}'
    except Exception as e:
        return f'Unknown error: {e}'


def find_ready(sources, timeout=0.05):
    """Find ready connections among a list of source connections."""
    try:
        connections, _, _ = select.select(sources, [], [], timeout)
        return connections
    except select.error:
        return []


@dataclass
class Server:
    """A socket server for doing remote maths."""

    host: str
    port: int
    backlog: int = 5
    message_size: int = 1024
    clients: dict = None

    def __post_init__(self):
        # Called after the dataclass' generated `__init__()`
        self.clients = []

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, *args):
        self.sock.close()

    @property
    def address(self) -> str:
        """Return the server's address."""
        return to_address(self.host, self.port)

    def start(self):
        """Start the server and run its main evaluation loop."""
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.backlog)
        print(f'Listening on {self.address}')

        self.running = True
        while self.running:
            self.poll()
            self.read_evaluate_respond()

    def poll(self):
        """Check and register new connections."""
        new_connections = find_ready([self.sock])
        for connection in new_connections:
            client, address = connection.accept()
            print('New connection from', to_address(*address))
            self.clients.append(client)

    def read_evaluate_respond(self):
        """Perform read/evaluate/respond for each registered client."""
        ready_clients = find_ready(self.clients)
        dead_clients = []

        for client in ready_clients:
            address = to_address(*client.getsockname())

            data: bytes = client.recv(self.message_size)

            if not data:
                print(f'Connection {address} closed by client.')
                client.close()
                dead_clients.append(client)
                continue

            message: str = data.decode()
            response: str = evaluate(message)

            client.sendall(response.encode())

            print({
                'connection': address,
                'received': message,
                'sent': response
            })

        if not dead_clients:
            return

        # Remove dead clients so they're not polled again in the future
        self.clients = [
            client for client in self.clients
            if client not in dead_clients
        ]


if __name__ == '__main__':
    host, port = from_argv()
    with Server(host=host, port=port) as server:
        try:
            server.start()
        except KeyboardInterrupt:
            pass
