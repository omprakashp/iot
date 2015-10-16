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

from iot.users.models import Devices
def get_autocar_mode():
    device = Devices.objects.filter(device_id='AutoCar')[0]
    mode = device.deviceproperties.mode
    return mode

def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))


def track(image):
    '''Accepts BGR image as Numpy array
       Returns: (x,y) coordinates of centroid if found
                (-1,-1) if no centroid was found
                None if user hit ESC
    '''

    # Blur the image to reduce noise
    blur = cv2.GaussianBlur(image, (5,5),0)

    # Convert BGR to HSV
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #Threshold the HSV image for only yellow colors
    #lower_green = np.array([20,100,100])
    #upper_green = np.array([30,255,255])

    #green
    #lower_green = np.array([40, 70, 70])
    #upper_green = np.array([80, 200, 200])

    #Blue
    #lower_green = np.array([100, 100, 100])
    #upper_green = np.array([120, 255, 255])

    #Red
    #lower_green = np.array([0, 0, 0])
    #upper_green = np.array([179, 255, 255])

    #pink
    lower_green = np.array([157, 72, 156])
    upper_green = np.array([180, 169, 255])

    #orange
    #lower_green = np.array([0, 100, 100], np.uint8)
    #upper_green = np.array([15, 255, 255], np.uint8)

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
        #print "centroid values", centroid_x, centroid_y
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
    print coordinates_list
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
            #next_direction = next_direction
     

    elif x_dec >= number_of_frames:
        if next_direction:
            next_direction = next_direction + ' & ' + 'right'
        else:
            print "STATIC"
            #next_direction = next_direction
          

    if next_direction:
        direction = next_direction

        print ">>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<", direction

    '''

    if x_inc >= number_of_frames and min_axis + 40 <= max_axis:
        if y_inc >= number_of_frames:
            direction = "reverse & right"
            #direction = "forward & right"
        elif y_dec >= number_of_frames:
            direction = "forward & left"
        
    elif x_dec >= number_of_frames and min_axis + 40 <= max_axis:
        if y_inc >= number_of_frames:
            direction = "reverse & left"
            #direction = "forward & right"
        elif y_dec >= number_of_frames:
            direction = "forward & right"
 
    elif x_inc >= number_of_frames:
        if y_inc >= number_of_frames:
            direction = "reverse"
            #direction = "forward"
        elif y_dec >= number_of_frames:
            direction = "forward"
            
    #elif len(x_values) != len(x_axis_set):
    #    print "Im here to stop3"
    #    #direction = direction
    #    direction = "stop"
    #else:    
    #    print "Im here to stop3"
    #    direction = "stop"
    '''

    return direction


def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf


def connection_accept(conn):
    print "Entered"
    j = 0
    collect_coordinates = []
    direction = ''
    old_direction = ''


    old_coordinates = (0,0)

    x_coordinates = []
    timer_start = 0
    stopped = 0
    while True:
        j = j+1
        length = recvall(conn,16)
        if not length:
            continue
        stringData = recvall(conn, int(length))
        data = np.fromstring(stringData, dtype='uint8')

        decimg=cv2.imdecode(data,1)

        cv2.imshow('SERVER',decimg)
        cv2.waitKey(1)

        coordinates = track(decimg)
        if not coordinates:
            print "Breakk"
            break
        else:
            if coordinates == (-1, -1):
                if not timer_start:
                     timer_start = time.time()
                else:
                    if time.time() - timer_start >= 7:
                        if not stopped:
                            if not TESTING:
                                car_mode = get_autocar_mode()
                                if car_mode == 'AUTO':
                                    print ''
                                    client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "stop", "speed":10}')
                            print "SSSSSSSSSSSSSSSSSSSTTTTTTTTTTTTTTTTOOOOOOOOOOOOOPPPPPPPPPPPP"
                            stopped = 1
                        continue
                print ">>>", x_coordinates
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
                print "VOTING", x_inc, x_dec
                if x_inc > x_dec:
                    #pass
                    direction = 'left'
                    print "INTELLIGENCE REPORT >>>>>>        LEFT LEFT"
                else:
                    #pass
                    direction = 'right'
                    print "INTELLIGnENCE REPORT >>>>>>        RIGHT RIGHT RIGHT"
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
                    speed = 100
                else:
                    speed = 30

                print "<<>>>>>", get_autocar_mode()
                car_mode = get_autocar_mode()
                if car_mode == 'AUTO':
                    
                    client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "%s", "speed":%s}' %(direction.strip(), speed))

            '''
            collect_coordinates.append(coordinates)
            if len(collect_coordinates) > 5:
                old_direction = direction
                direction = compute_direction(collect_coordinates, direction)
                collect_coordinates = []
                if direction == "NOACTION":
                    continue
               #if direction in ['forward', 'reverse', 'stop'] and direction == old_direction:
                #    print "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^6", direction
                #    continue
                if "&" in direction:
                    directions = direction.split()
                else:
                    directions = [direction]
                #TODO:
                for direction in directions:
                    pass
                    #print "FINAL DESTINATION >>>>>>>>>>>>>>>>>> ", direction
                    #client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "%s", "speed":30}' %direction.strip())
            '''                

if __name__ == "__main__":

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

