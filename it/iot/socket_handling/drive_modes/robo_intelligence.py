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



import socket
import cv2
import numpy as np
import time
#TODO:  After left/right command from server.. Decide hw many frames to skip / handle frames not to give opp direction command
#	when vehicle moves!

import paho.mqtt.client as mqtt

TESTING = False

from iot.users.models import Devices, User
from django.utils.functional import cached_property


def get_autocar_mode():
    #return ("AUTO", "FOLLOW")
    device = Devices.objects.filter(device_id='AutoCar')[0]
    mode = device.deviceproperties.mode
    drive_mode = device.deviceproperties.drive_mode
    return (mode, drive_mode)

def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))

def track(image):

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    #pink
    lower_green = np.array([157, 72, 156])
    upper_green = np.array([180, 169, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    
    # Blur the mask
    bmask = cv2.GaussianBlur(mask, (5,5),0)

    # Take the moments to get the centroid
    moments = cv2.moments(bmask)
    m00 = moments['m00']
    centroid_x, centroid_y = None, None
    if m00 != 0:
        centroid_x = int(moments['m10']/m00)
        centroid_y = int(moments['m01']/m00)
    # Assume no centroid
    ctr = (-1,-1)

    # Use centroid if it exists
    if centroid_x != None and centroid_y != None:

        ctr = (centroid_x, centroid_y)

        # Put black circle in at centroid in image
        cv2.circle(image, ctr, 50, (0,0,255))

    # Display full-color image
    #cv2.imshow(WINDOW_NAME, image)
    cv2.imshow('SERVER',image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid

    return ctr

def compute_direction(coordinates_list, direction):
    if len(list(set(coordinates_list))) == 1 and (-1, -1) in coordinates_list:
        direction = "stop"
        return direction

    elif (-1, -1) in coordinates_list:
        return "NOACTION"

    x_inc = 0
    x_dec = 0
    y_inc = 0
    y_dec = 0

    x_values, y_values = zip(*coordinates_list)
    for i in range(len(x_values)):
        try:
            if x_values[i] < x_values[i+1]:
                x_inc = x_inc + 1
            else:
                x_dec = x_dec + 1

            if y_values[i] < y_values[i+1]:
                y_inc = y_inc + 1
            else:
                y_dec = y_dec + 1

        except:
            pass

    number_of_frames = 3 #out of 10
    min_axis = min(x_values)
    max_axis = max(x_values)
    min_y_axis = min(x_values)
    max_y_axis = max(x_values)

    x_axis_set = list(set(x_values))
    y_axis_set = list(set(y_values))

    next_direction = ''
    
    if  y_dec >= number_of_frames:
        next_direction = 'forward'
    #else:
    #    direction = 'reverse'

    if x_inc >= number_of_frames:
        if next_direction:
            next_direction = next_direction + ' & ' + 'left'
        else:
            print "STATIC"

    elif x_dec >= number_of_frames:
        if next_direction:
            next_direction = next_direction + ' & ' + 'right'
        else:
            print "STATIC"
          

    if next_direction:
        direction = next_direction

    return direction


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
        client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "left", "speed":30}')
        client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "forward", "speed":30}')
        if send:
            message = "Obstacles detected! You wanna take Manual control??"
            payload = {"device_type": "autocar", "device_id":"AutoCar"}
            device = Devices.objects.filter(device_id='AutoCar')[0]
            mobile_device = User.objects.get(email=device.owner).gcm_device
            mobile_device.send_message(message, extra=payload)
            print "Sent Push Notification"
            
    except Exception, e:
        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", str(e)


def connection_accept(conn):
    collect_coordinates = []
    direction = ''
    old_direction = ''
    old_coordinates = (0,0)
    x_coordinates = []
    timer_start = 0
    stopped = 0

    #AVOID MODE ASSIGNMENTS
    sent_time = 0 #for push notifications

    def shutdown_windows():
        try:
            cv2.destroyAllWindows()
            print "Destroyed all windows"
        except Exception, e:
            print "Exception while closing the IM", str(e)


    while True:
        time.sleep(0.05)
        car_mode, drive_mode = get_autocar_mode()
        if not car_mode == 'AUTO':
            #shutdown_windows()
            continue 
        #drive_mode = 'AVOID'
        if drive_mode not in ['FOLLOW']: #removed avoid mode
            #shutdown_windows()
            continue
        length = recvall(conn,16)
        if not length:
            continue
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype='uint8')

        frame=cv2.imdecode(data,1)
         
        if drive_mode == 'FOLLOW':
            cv2.imshow('SERVER',frame)
            cv2.waitKey(1)
 
            coordinates = track(frame)
            if not coordinates:
                print "Breakk"
                break
            else:
                if coordinates == (-1, -1):
                    if not timer_start:
                         timer_start = time.time()
                    else:
                        if time.time() - timer_start >= 3:
                            if not stopped:
                                if not TESTING:
                                    client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "stop", "speed":50}')
                                stopped = 1
                            continue
                    x_inc = 0
                    x_dec = 0
                    for i in range(len(x_coordinates)):
                        try:
                            if x_coordinates[i] < x_coordinates[i+1]:
                                x_inc = x_inc + 1
                            else:
                                x_dec = x_dec + 1
                        except:
                            pass
                    if x_inc > x_dec:
                        #pass
                        direction = 'right'
                    else:
                        #pass
                        direction = 'left'
                else:
                    timer_start = 0
                    stopped = 0
                    direction = 'forward'
                    if len(x_coordinates) > 3:
                        x_coordinates.pop(0)
                    x_coordinates.append(coordinates[0])
 
                    #Logic to stop
 
                if not TESTING:
                    if direction == 'forward':
                        speed = 50
                    else:
                        speed = 50
 
                    client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "%s", "speed":%s}' %(direction.strip(), speed))

        '''
        elif drive_mode == "AVOID":
            image = frame
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
                            if time.time() - sent_time > 60:
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
        '''

if __name__ == "__main__":

    client = mqtt.Client("robo")
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("10.99.90.32", 1883, 3600)

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
            s = socket.socket()         # Create a socket object
            host = '10.99.90.32'#socket.gethostname() # Get local machine name
            if not TESTING:
                port = 5007                # Reserve a port for your service
            else:
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
            connection_accept(c)
        except:
            pass

