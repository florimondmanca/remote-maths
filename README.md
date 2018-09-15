# Remote Maths

Networking app allowing clients to do remote maths in a simple REPL.

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
Listening on localhost:4043
```

In another terminal session, you can start a client and start doing some maths:

```bash
$ python client.py
> 2**3
8
```

To stop either the server or a client, simply use `Ctrl+C`.

## Security

The app is protected against memory/CPU attacks and potentially harmful function calls:

```
> 9**9**9**9**9
Invalid expression: Sorry! I don't want to evaluate 9 ** 387420489
> open('nasty.txt')
Invalid expression: Function 'open' not defined, for expression 'open('nasty.txt')'.
```
