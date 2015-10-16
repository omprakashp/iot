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


def find_blue_ball_in_image(conn):

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
            #client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "left", "speed":70}')
            #client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "forward", "speed":30}')
            if send:
                message = "Obstacles detected! You wanna take Manual control??"
                payload = {"device_type": "autocar", "device_id":"AutoCar"}
                device = Devices.objects.filter(device_id='AutoCar')[0]
                #mobile_device = User.objects.get(email=device.owner).gcm_device
                #mobile_device.send_message(message, extra=payload)
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
        frame=cv2.imdecode(data,1)

        #frame = cv2.imread(imagepath)

        # convert to hsv
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        def find_colored_object(color):
            found = False
            # define blue range
            if color == 'blue':
                lower = np.array([90, 50, 50], dtype=np.uint8)
                upper = np.array([130, 255, 255], dtype=np.uint8)
            elif color == 'red':
                lower = np.array([170,160,60], dtype=np.uint8)
                upper = np.array([180,255,255], dtype=np.uint8)
            elif color == 'green':
                lower = np.array([38, 50, 50], dtype=np.uint8)
                upper = np.array([75, 255, 255], dtype=np.uint8)
            elif color == 'black':
                lower = np.array([0, 0, 0], dtype=np.uint8)
                upper = np.array([15, 15, 15], dtype=np.uint8)
            elif color == 'yellow':
                lower = np.array([20,100,100], dtype=np.uint8)
                upper = np.array([40,255,255], dtype=np.uint8)
            elif color == 'pink':
                lower = np.array([157, 72, 156])
                upper = np.array([180, 169, 255])

             # threshold to only get blue
            mask = cv2.inRange(hsv, lower, upper)

            # bitwise and mask the original
            res = cv2.bitwise_and(frame, frame, mask=mask)

            # split into channels, we keep saturation channel
            (h, s, v) = cv2.split(res)

            # blur it
            blur = cv2.medianBlur(s, 5)

            # erode image
            el = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (10, 10))
            tmp = cv2.erode(blur, el, iterations=1)

            # threshold and detect edges
            (_, tmp2) = cv2.threshold(tmp, 0, 255, cv2.THRESH_BINARY)
            edges = cv2.Canny(tmp2, 100, 100)

            # find contours, we use edges here but could also use tmp2
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            output = frame.copy()
            for contour in contours:
                approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

                # is contour not convex it is probably not a circle
                if not cv2.isContourConvex(approx):
                    continue

                area = cv2.contourArea(contour)
                center, radius = cv2.minEnclosingCircle(contour)
                tmp = 1 - (area / (math.pi * math.pow(radius, 2)))
                if tmp < 0.2:

                    # we found a circle, draw contours
                    #draw circle if radius > 10
                    if radius > 20:
                        found = "True"
                        try:
                            cv2.drawContours(output, [contour], 0, (0, 0, 0), 3)
                        except Exception, e:
                            print "ERRRRRRRRRRRRRRRRRRR", str(e)
            cv2.imshow("blue", output)
            cv2.waitKey(1)
            if found:
                print "FOUND"
                return True
            else:
                return False



        colors = ["blue"]
        sent = 0
        for color in colors:
            result = find_colored_object(color)
            if result == True:
                if get_autocar_mode() == 'AUTO':
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
                port = 5006                # Reserve a port for your service
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
            find_blue_ball_in_image(c)
        except:
            pass


