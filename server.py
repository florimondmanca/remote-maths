import socket
from time import sleep
from simpleeval import simple_eval, InvalidExpression


def to_address(host, port) -> str:
    return f'{host}:{port}'


def evaluate(expression: str) -> str:
    try:
        return str(simple_eval(expression))
    except InvalidExpression as e:
        return f'Invalid expression: {e}'
    except SyntaxError as e:
        return f'Syntax error: {e}'
    except Exception as e:
        return f'Unknown error: {e}'


def run_forever(host: str, port: int,
                listeners: int = 1, message_size: int = 1024):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(listeners)

        print(f'Listening on {host}:{port}')

        connection, connection_host_and_port = sock.accept()
        address = to_address(*connection_host_and_port)

        with connection:
            print('New connection:', address)
            while True:
                data: bytes = connection.recv(message_size)

                if not data:
                    print(f'Connection {address} closed by client.')
                    break

                message: str = data.decode()
                response: str = evaluate(message)

                connection.sendall(response.encode())

                print({
                    'connection': address,
                    'received': message,
                    'sent': response
                })


if __name__ == '__main__':
    try:
        run_forever(host='localhost', port=4043)
    except KeyboardInterrupt:
        print('Exited')
