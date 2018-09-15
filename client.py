import socket


def run(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            message = input('> ')
            sock.sendall(message.encode()[:1024])
            response: str = sock.recv(1024).decode()
            if not response:
                print('Connection closed by server.')
                return
            print(response)


if __name__ == '__main__':
    try:
        run(host='localhost', port=4042)
    except KeyboardInterrupt:
        pass
