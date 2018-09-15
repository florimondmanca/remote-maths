"""Maths client.

Usage:
$ python client.py [server_address=$MATHS_SERVER_ADDRESS|localhost:4042]
"""

import socket

from address import from_argv, to_address

PROMPT = '>>> '


def run(host: str, port: int):
    """Run the maths client."""
    address = to_address(host, port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))

        print(f'Connected to {address}')

        while True:
            message = input(PROMPT)
            sock.sendall(message.encode()[:1024])

            response: str = sock.recv(1024).decode()

            if not response:
                print('Connection closed by server.')
                return

            print(response)


if __name__ == '__main__':
    host, port = from_argv()
    try:
        run(host=host, port=port)
    except KeyboardInterrupt:
        pass
