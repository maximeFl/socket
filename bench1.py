# benchmark 1 
# 
from socket import *
from threading import Thread
import time

n = 0

def count_ops():
   while True:
       time.sleep(1)
       global n
       print("{} ops per sec".format(n))
       n = 0

t = Thread(target=count_ops, args=(),)
t.daemon = True
t.start()
del t

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', 25000))


while True:
    sock.send(b'1')
    resp = sock.recv(100)
    n += 1
