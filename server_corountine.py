# server.py
# Fib microservice
from fib import fib
import socket
from collections import deque
from select import select
tasks = deque()
recv_wait = {} # Mapping sockets -> tasks
send_wait = {}

def run():
    while any([tasks, recv_wait, send_wait]):
        while not tasks:
            # wait for I/O
            can_recv, can_send, []  = select(recv_wait, send_wait, [])
            for s in can_recv:
                tasks.append(recv_wait.pop(s))
            for s in can_send:
                tasks.append(send_wait.pop(s))
        task = tasks.popleft()
        try:
            why, what = next(task)
            if why == 'recv':
                recv_wait[what] = task
            elif why == 'send':
                send_wait[what] = task
            else:
                raise RuntimeError("ARG!")
        except StopIteration:
            print("Task done")

def fib_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        yield 'recv', sock
        client, addr = sock.accept() #Block
        print("Connection", addr)
        tasks.append(fib_handler(client))

def fib_handler(client):
    while True:
        yield 'recv', client
        req = client.recv(100) # Block
        if not req:
            break
        n = int(req)
        resp = fib(n)
        resp = str(resp).encode('ascii') +b'\n'
        yield 'send', client
        client.send(resp) #block
    print("Closed")

tasks.append(fib_server(('', 25000)))
