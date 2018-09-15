# Remote Calculator

Networking app allowing clients to do remote maths in a friendly REPL.

## Install

The REPL relies on [simpleeval]() to safely evaluate expressions.

To install it, simply install the requirements:

```bash
$ pip install -r requirements.txt
```

## Quickstart

In a terminal session, start the server:

```bash
$ python server.py
Listening on localhost:4043
```

In another terminal session, you can start a client and do some maths:

```bash
$ python client.py
> 2**3
8
```

## Security

The app is protected against memory/CPU attacks and potentially harmful function calls:

```
> 9**9**9**9**9
Invalid expression: Sorry! I don't want to evaluate 9 ** 387420489
> open('nasty.txt')
Invalid expression: Function 'open' not defined, for expression 'open('nasty.txt')'.
```
