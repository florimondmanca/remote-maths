import socket


def run_forever(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port))
        while True:
            message = input('> ')
            sock.sendall(message.encode())
            response: str = sock.recv(1024).decode()
            print(response)


if __name__ == '__main__':
    try:
        run_forever(host='localhost', port=4043)
    except KeyboardInterrupt:
        print('Bye!')
