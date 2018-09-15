"""Maths server."""

import select
import socket
from dataclasses import dataclass

from utils import to_address
from simpleeval import InvalidExpression, simple_eval


def evaluate(expression: str) -> str:
    try:
        return str(simple_eval(expression))
    except InvalidExpression as e:
        return f'Invalid expression: {e}'
    except SyntaxError as e:
        return f'Syntax error: {e}'
    except Exception as e:
        return f'Unknown error: {e}'


def find_ready(sources, timeout=0.05):
    try:
        connections, _, _ = select.select(sources, [], [], timeout)
        return connections
    except select.error:
        return []


@dataclass
class Server:

    host: str
    port: int
    listeners: int = 1
    message_size: int = 1024
    clients: dict = None

    def __post_init__(self):
        self.clients = []

    def __enter__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return self

    def __exit__(self, *args):
        self.sock.close()

    @property
    def address(self):
        return to_address(self.host, self.port)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(self.listeners)
        print(f'Listening on {self.address}')

        self.running = True
        while self.running:
            self.poll()
            self.read_and_answer()

    def poll(self):
        new_connections = find_ready([self.sock])
        for connection in new_connections:
            client, address = connection.accept()
            print('New connection from', to_address(*address))
            self.clients.append(client)

    def read_and_answer(self):
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
    with Server(host='localhost', port=4042) as server:
        try:
            server.start()
        except KeyboardInterrupt:
            pass
