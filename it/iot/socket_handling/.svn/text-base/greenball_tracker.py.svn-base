#!/usr/bin/env python


#mqtt modules imports
import paho.mqtt.client as mqtt
def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))


import cv2
import numpy as np
from datetime import datetime

# For OpenCV2 image display
WINDOW_NAME = 'GreenBallTracker' 

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
    lower_green = np.array([20,100,100])
    upper_green = np.array([40,255,255])
    # Threshold the HSV image to get only pink colors
    #lower_green = np.array([40, 70, 70])
    #upper_green = np.array([80, 200, 200])
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
        cv2.circle(image, ctr, 4, (0,0,0))

    # Display full-color image
    cv2.imshow(WINDOW_NAME, image)

    # Force image display, setting centroid to None on ESC key input
    if cv2.waitKey(1) & 0xFF == 27:
        ctr = None
    
    # Return coordinates of centroid

    return ctr

def compute_direction(coordinates_list, direction):
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

    if -1 in x_axis_set or -1 in y_axis_set :
        direction = direction

    elif x_inc >= number_of_frames:
        if min_axis + 40 <= max_axis:
            direction = "left"
            
            if y_inc >= number_of_frames and min_y_axis + 10 <= max_y_axis:
                direction = "reverse & left"
            elif y_dec >= number_of_frames and  min_y_axis + 10 <= max_y_axis:
                direction = "forward & left"
            else:
                direction = "left"
        else:
            if y_inc >= number_of_frames and min_y_axis + 20 <= max_y_axis:
                direction = "reverse"
            elif y_dec >= number_of_frames and  min_y_axis + 20 <= max_y_axis:
                direction = "forward"
            else:
                direction = "stop"
            

    elif  x_dec >= number_of_frames:
        if min_axis + 40 <= max_axis:
            if y_inc >= number_of_frames and min_y_axis + 10 <= max_y_axis:
                direction = "reverse & right"
            elif y_dec >= number_of_frames and min_y_axis + 10 <= max_y_axis:
                direction = "forward & right"
            else:
                direction = "right"
        else:
            if y_inc >= number_of_frames and min_y_axis + 20 <= max_y_axis:
                direction = "reverse"
            elif y_dec >= number_of_frames and min_y_axis + 20 <= max_y_axis:
                direction = "forward"
            else:
                direction = "stop"
    else:
        if len(x_values) != len(x_axis_set):
            direction = "stop"

    return direction
# Test with input from camera
if __name__ == '__main__':
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_publish = on_publish
    client.connect("10.99.90.32", 1883, 60)

    capture = cv2.VideoCapture(0)


    collect_coordinates = []
    direction = ''
    old_direction = ''
    i = 0
    while True:
        i = i+1
        okay, image = capture.read()

        if okay:
            coordinates = track(image)
            if not coordinates:
                break
            else:
                collect_coordinates.append(coordinates)
                if len(collect_coordinates) > 4:
                    old_direction = direction
                    direction = compute_direction(collect_coordinates, direction)
                    if direction in ['forward', 'reverse', 'stop'] and direction == old_direction:
                        continue
                    if "&" in direction:
                        directions = direction.split()
                    else:
                        directions = [direction]
                    for direction in directions:
                        print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", direction
                        client.publish("emb/iot/autocar", '{"device_id":"AutoCar", "command": "%s", "speed":30}' %direction.strip())
                    collect_coordinates = []
                
            if cv2.waitKey(1) & 0xFF == 27:
                break

        else:

           print('Capture failed')
           break
