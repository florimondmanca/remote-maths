"""Socket address utility functions."""

import sys
import os

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 4042


def parse(address: str):
    """Parse the host and port from a `host:port` address string."""
    try:
        host, port = address.split(':')
        return host, int(port)
    except ValueError as e:
        raise ValueError(f'{address} is not a valid host:port address') from e


def to_address(host: str, port: int) -> str:
    """Convert a host and port to their `host:port` string representation."""
    return f'{host}:{port}'


def from_argv(default_host='localhost', default_port=4042):
    """Get host and port from the first command line argument."""
    if len(sys.argv) > 1:
        host, port = parse(sys.argv[1])
    elif 'MATHS_SERVER_ADDRESS' in os.environ:
        host, port = parse(os.environ.get('MATHS_SERVER_ADDRESS'))
    else:
        host, port = default_host, default_port
    return host, port
