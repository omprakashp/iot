#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python
import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

try:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")
except:
    pass

import django
django.setup()



# -*- coding: utf-8 -*-
import  socket
import cv2
import numpy as np
import math
import time
import paho.mqtt.client as mqtt

TESTING = False


from iot.users.models import Devices, User
def get_autocar_mode():
    return "AUTO"
    device = Devices.objects.filter(device_id='AutoCar')[0]
    mode = device.deviceproperties.mode
    return mode


def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))


def find_circles_in_image(conn):

    def recvall(sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


    def take_diversion(send):
        #send flag is for pushnotifications.. when obstacle is found send PN
        try:
            client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "left", "speed":100}')
            client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "left", "speed":100}')
            client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "left", "speed":100}')
            client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "forward", "speed":10}')
            if send:
                message = "Obstacles detected! You wanna take Manual control??"
                payload = {"device_type": "autocar", "device_id":"AutoCar"}
                device = Devices.objects.filter(device_id='AutoCar')[0]
                mobile_device = User.objects.get(email=device.owner).gcm_device
                mobile_device.send_message(message, extra=payload)
                print "Sent Push Notification"
                
        except Exception, e:
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", str(e)

    i = 0
    sent_time = 0 #for push notifications
    while True:
        i = i+1

        length = recvall(conn,16)
        if not length:
            continue
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype='uint8')
        image=cv2.imdecode(data,1)

        output = image.copy()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
        # detect circles in the image
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 120)
 
        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
 
            # loop over the (x, y) coordinates and radius of the circles
            for (x, y, r) in circles:
                # draw the circle in the output image, then draw a rectangle
                # corresponding to the center of the circle
                cv2.circle(output, (x, y), r, (0, 255, 0), 4)
                cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                print "r", r
                if r > 40:
                    if sent_time:
                        if time.time() - sent_time > 10:
                            send = True
                            sent_time = time.time()
                        else:
                            send = False
                    else:
                        send = True
                        sent_time = time.time()
                    take_diversion(send)
                   
                    break


                    
        cv2.imshow("output", np.hstack([image, output]))
        cv2.waitKey(1)


if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("10.99.90.32", 1883, 60)

    while True:
        try:
            print "close c"
            c.close()
            print "close s"
            s.close()
            try:
                print "Destroying all windows"
                cv2.destroyAllWindows()
                print "Destroyed all windows"
            except Exception, e:
                print "Exception while closing the IM"
        except Exception, e:
            print "Exception Here", str(e)

        try:
            print "opening new socket"
            s = socket.socket()         # Create a socket object
            host = '10.99.90.32'#socket.gethostname() # Get local machine name
            if not TESTING:
                port = 5007                # Reserve a port for your service
            else:
                host = '192.168.1.110'#socket.gethostname() # Get local machine name
                port = 5005                # Reserve a port for your service
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))        # Bind to the port

            s.listen(5)                 # Now wait for client connection.
            c, addr = s.accept()     # Establish connection with client.
        except Exception, e:
            print "ERROR IN BINDING", str(e)
            time.sleep(5)
            continue



        try:
            find_circles_in_image(c)
        except:
            pass


