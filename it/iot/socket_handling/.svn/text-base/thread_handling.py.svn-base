#!/usr/bin/python
import threading
import time

def my_service():
    time.sleep(1)
    print 1234

t = threading.Thread(name='my_service', target=my_service)
t.start()
