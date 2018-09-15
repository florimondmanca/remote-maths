def parse_host_and_port(address: str):
    try:
        host, port = address.split(':')
        return host, port
    except ValueError:
        raise ValueError(f'{address} is not a valid host:port address')


def to_address(host: str, port: int) -> str:
    return f'{host}:{port}'
