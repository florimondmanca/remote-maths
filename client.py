"""Maths client."""

import sys
import socket
from utils import parse_host_and_port, to_address


def run(host: str, port: int):
    address = to_address(host, port)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        print(f'Connected to {address}')
        while True:
            message = input('>>> ')
            sock.sendall(message.encode()[:1024])
            response: str = sock.recv(1024).decode()
            if not response:
                print('Connection closed by server.')
                return
            print(response)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        host, port = parse_host_and_port(sys.argv[1])
    else:
        host, port = 'localhost', 4042

    try:
        run(host=host, port=port)
    except KeyboardInterrupt:
        pass
