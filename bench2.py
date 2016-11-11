import time
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))

while True:
    start = time.time()
    sock.send(b'31')
    sock.recv(100)
    end = time.time()
    print("{} seconds".format(end - start))
