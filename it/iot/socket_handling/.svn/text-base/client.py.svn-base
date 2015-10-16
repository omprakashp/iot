#!/usr/bin/python           # This is client.py file

import threading
import socket               # Import socket module

s = socket.socket()         # Create a socket object
host = '10.99.90.32' #socket.gethostname() # Get local machine name
port = 5006                # Reserve a port for your service.

s.connect((host, port))



def my_service():

    import time
    for i in range(10):
        time.sleep(5)
        if i%2 == 0:
            action = 'ON'
        else:
            action = 'OFF'
        s.send('{"ON / OFF": "%s", "device_id": "ABCD1234"}' %action)


t = threading.Thread(name='my_service', target=my_service)
t.start()       


while True:
    data = s.recv(1024)
    if data:
        print data


