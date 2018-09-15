# Remote Maths

Networking app allowing one or more clients to do remote maths in a secure REPL.

*Built as part of tinkering with lower-level socket programming in Python.*

## Install

The REPL relies on [simpleeval](https://github.com/danthedeckie/simpleeval) to safely evaluate expressions.

To install it, use the requirements file:

```bash
$ pip install -r requirements.txt
```

## Quickstart

In a terminal session, start the server:

```bash
$ python server.py
Listening on localhost:4042
```

In another terminal session, you can start a client and start doing some maths:

```bash
$ python client.py
Connected to localhost:4042
>>> 2**3
8
```

Optionally, you can also pass the server's address through a command line argument or the `REMOTE_MATHS_SERVER_ADDRESS` environment variable.

To stop either the server or a client, simply use `Ctrl+C`.

## Configuration

For both the server and the client, you can specify the server's address through a command line argument or the `REMOTE_MATHS_SERVER_ADDRESS` environment variable (note that using a host name different than `localhost` is likely to fail):

```bash
$ python server.py localhost:8000
Listening on localhost:8000
^C
$ export REMOTE_MATHS_SERVER_ADDRESS=8001
$ python server.py
Listening on localhost:8001
```

```bash
$ python client.py localhost:8001
Connected to localhost:8001
>>>
```

## Security

The app is protected against memory/CPU attacks and potentially harmful function calls:

```
> 9**9**9**9**9
Invalid expression: Sorry! I don't want to evaluate 9 ** 387420489
> open('nasty.txt')
Invalid expression: Function 'open' not defined, for expression 'open('nasty.txt')'.
```
