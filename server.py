# server.py
# Fib microservice
from fib import fib
from socket import *
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

pool = Pool(4)

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("Connection", addr)
        t = Thread(target=fib_handler, args=(client,))
        t.start()

def fib_handler(client):
    while True:
        req = client.recv(100)
        if not req:
            break
        n = int(req)
        future = pool.submit(fib, n)
        resp = future.result() 
        resp = str(resp).encode('ascii') +b'\n'
        client.send(resp)
    print("Closed")

fib_server(('', 25000))
