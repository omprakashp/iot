import threading
import time
import requests
import json
import re
import sys, os
sys.path.append(os.path.abspath('..'))
sys.path.append('/var/www/www.embitel.com/it/iot')
sys.path.append('/var/www/www.embitel.com/it/')
import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()

from iot.users.models import SocketCommands, DevicesData, Devices, User, UserEvents, AutoCar
from iot.views import send_push_notification


import paho.mqtt.client as mqtt


#NLP
from nltk.tokenize import word_tokenize

from nltk.tag import pos_tag
from django.db.models import Q

colors = {"red": "#FF0000", "blue": "#0000FF", "green": "#00FF00", "white": "#FFFFFF", "yellow": "#FFFF00", "silver": "#C0C0C0", "gray": "#808080", "maroon": "#800000", "purple": "#800080", "gold": "#FFD700"}

def get_autocar_mode():
    #return ("AUTO", "FOLLOW")
    device = Devices.objects.filter(device_id='AutoCar')[0]
    mode = device.deviceproperties.mode
    drive_mode = device.deviceproperties.drive_mode
    return (mode, drive_mode)


#Process voice/text commands from mobile application
def process_voice_commands(data):
    print "Got data >", data

    if 'AUTOCAR_NLP:' in data:
        mode = ''
        drive_mode = ''
        message = ''
        data = data.replace('AUTOCAR_NLP:', '').lower()
        if 'manual' in data:
            mode = 'MANUAL'
        elif 'auto' in data or 'autonomous' in data:
            mode = 'AUTO'

        if 'follow' in data:
            drive_mode = 'FOLLOW'
        elif 'avoid' in data:
            drive_mode = 'AVOID'
        elif 'lane' in data:
            drive_mode = 'LANE'
        
        print "Before >>>>>>>", data, mode, drive_mode

        device = Devices.objects.filter(device_type__name__contains='autocar')[0]
        if mode == '' or drive_mode == '':
            #for user specific control please use owner in the query
            device = Devices.objects.filter(device_type__name__contains='autocar')[0]
            properties = device.deviceproperties
            if not mode:
                mode = properties.mode
            else:
                message = 'Changed transmission mode to %s' %mode
            if not drive_mode:
                print "Im hereeeeeeeeeeeeee"
                drive_mode = properties.drive_mode
            else:
                print "Im hereeeeeeeeeeeeeeeeeeeeeeeee"
                if not message:
                    message = 'Changed drive mode to %s' %drive_mode
                else:
                    message = message + ' and drive mode to %s' % drive_mode
        else:
            message = 'Changed transmission mode to %s and drive mode to %s' % (mode, drive_mode)

        if not message:
            message = 'Failed to update transmission or drive modes!'
               
        modes_transmission_url = 'http://tatatrent.embdev.in/mobile/devices/autocar_mode/'
        payload = {"email": device.owner, "mode": str(mode), "drive_mode": str(drive_mode)}
        r = requests.post(modes_transmission_url, data=json.dumps(payload))
  
        payload['message'] = message 
        client.publish("emb/iot/notifications/", "%s" %(str(payload))) 
        print payload

        return

    #Implement at user level, data should have registered email id
    data = data.lower().replace('shut down', 'shutdown')
    words = word_tokenize(data)
    handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'

    #### FUN PART
    if 'what' and 'colours' in words:
        message = 'I can only set one of these colors! %s' %(', '.join(colors.keys()))
        client.publish("emb/iot/notifications/", "%s" %(message)) 
        return
    ####

    if "trigger" in data:
        data = data.replace('the', '')
        event_name = re.findall('trigger (.*)', data)
        if event_name[0].strip():
            event_name = event_name[0].strip()
        try:
            event = UserEvents.objects.get(name__icontains=event_name) 
            payload =  {"email": event.user.email, "event":event.id }
            r = requests.post(handle_events_url, data=json.dumps(payload))
            message = 'Event "%s" has been triggered!' %event.name
            client.publish("emb/iot/notifications/", "%s" %(message)) 
        except Exception, e:
            print str(e), event_name
            message = 'No such event found! Please try again!'
            client.publish("emb/iot/notifications/", "%s" %(message)) 
        return

    if "all" in data and 'lights' in data:
        if "on" in data:
            action = 'ON'
        elif 'off' in data or 'shutdown' in data:
            action = 'OFF'
        else:
            action = 'ON'
        #Hardcoded!
        payload = {'device_category': "my_office", 'device_type':"office_light", 'DIM': '100', 'ON / OFF': action, 'device_id': "G000", 'Current Color': "#FFFFFF"}
        color_flag = False
        ####if 'colour' in words:
        available_colors = colors.keys()
        for available_color in available_colors:
            if available_color in words:
                color_flag = True
                payload['Current Color'] = colors[available_color]
                break
        print payload
        sc = SocketCommands.objects.create()
        sc.command = str(json.dumps(payload))
        sc.save()
        message = 'I turned "%s" all the lights!' %action
        if color_flag:
            message = message + ' And changed the color to %s' %available_color
        if 'colour' in words and not color_flag:
            message = 'Sorry! I couldn\'t set the mentioned color! Please try some other colors!' 
        client.publish("emb/iot/notifications/", "%s" %(message)) 
        return

    parts_of_speech = pos_tag(words)
    nouns = []
    verbs = []
    for part in parts_of_speech:
        if 'NN' in part[1]:
            if part[0] in ['turn', 'close', 'off', 'shutdown']:  #use some other postagger to get better results!
                verbs.append(part[0])
            elif part[0] in ['switch']:  #use some other postagger to get better results!
                verbs.append(part[0])
                nouns.append(part[0])
            else:
                nouns.append(part[0])
        else:
            verbs.append(part[0])
    print nouns
    print verbs
    words = data.split()
    query_part = ''
    if not nouns:
        message = 'No device name found! Please try again!'
        client.publish("emb/iot/notifications/", "%s" %(message)) 
        return
    query_parts = []
    for noun in nouns:
        query_parts.append('Q(device_name__icontains="%s")'%noun)

    concat_query = ' | '.join(query_parts)
    devices_query = 'Devices.objects.filter(%s, owner__startswith="madhujeet")' %concat_query
    print devices_query
    devices = eval(devices_query)
    nlp_device = ''
    for device in devices:
        device_name = device.device_name.lower()
        device_name_split = device_name.split()
        matching_count = 0
        for word in device_name_split:
            if word in words:
                matching_count = matching_count + 1
        if matching_count  >= len(device_name_split):
            nlp_device = device
            break
    device = nlp_device

    if not device:
        print "No device found"
        nlp_device_found = False
        message = 'No such device found! Please try again!'
        client.publish("emb/iot/notifications/", "%s" %(message)) 
        return

    action = ''
    #Action detection
    if 'blind' in device.device_type.name:
        if 'open' in verbs:
            action = 'OPEN'
        elif 'close' in verbs or  'shutdown' in verbs: 
            action = 'CLOSE'
    else:
        if 'on' in verbs:
            if len(verbs) == 1:
                action = 'ON'
            else:
                if 'turn' in verbs or 'switch' in verbs:
                    action = 'ON'
        if 'off' in verbs:
            action = 'OFF'
    print "ACTION>>>>>>>>>>>>>>>>>", action

    #FOllowing logic is for setting the color to lamps
    if 'light' in device.device_type.name:
        payload = {}
        if action:
            payload = {'category': device.device_type.device_category.name, 'DIM': '100', 'ON / OFF': action, 'id': device.id, 'device_id': device.device_id, 'email':device.owner, 'Current Color': '#ffffff'}
            message = 'I changed "%s" current state to "%s"!' %(device.device_name, action)

        color_flag = False
        available_colors = colors.keys()
        for available_color in available_colors:
            if available_color in words:
                if not payload:
                    payload = {'category': device.device_type.device_category.name, 'DIM': '100', 'ON / OFF': action, 'id': device.id, 'device_id': device.device_id, 'email':device.owner, 'Current Color': '#ffffff'}
                action = 'ON'
                color_flag = True
                payload['ON / OFF'] = 'ON'
                payload['Current Color'] = colors[available_color]
                message = 'I changed "%s" color to "%s"!' %(device.device_name, available_color.upper())
                print "message published", message
                break 
        if 'colour' in words:
            if color_flag == False:
                message = 'Sorry! I couldn\'t set the mentioned color! Please try some other colors!' 
                client.publish("emb/iot/notifications/", "%s" %(message)) 
                return
        if action:
            r = requests.post("http://tatatrent.embdev.in/mobile/devices/configure/", data=json.dumps(payload))
            client.publish("emb/iot/notifications/", "%s" %(message)) 
            return
        else:
            print "Whats happening here>>>>>>>>>>>>>>>>>>>>>>"
       #else:
        #    #No color found
        #    message = 'Sorry! I couldn\'t perform the command, as it is ambiguous!' 
        #    client.publish("emb/iot/notifications/", "%s" %(message)) 
        #    print "message published", message
        #return
                
    if not action:
        message = 'Your device "%s" current state is "%s! Please tell me any action to perform!"' %(device.device_name, device.current_state)
        client.publish("emb/iot/notifications/", "%s" %(message)) 
        return
            
    if "switch" in device.device_type.name:
        payload =  {"email": device.owner, "category":device.device_type.device_category.name, "device_id": device.device_id, "ON / OFF": action}
        r = requests.post("http://tatatrent.embdev.in/mobile/devices/configure/", data=json.dumps(payload))
        print "switch triggered"
    elif 'blind' in device.device_type.name:
        payload = {"category": device.device_type.device_category.name, "Slats": action, "Blinds": "CLOSE", "id": device.id, "device_id": device.device_id, "email":device.owner}
        r = requests.post("http://tatatrent.embdev.in/mobile/devices/configure/", data=json.dumps(payload))
        print "Blinds triggered"
    else:
        payload = {"category": device.device_type.device_category.name, "ON / OFF": action, "id": device.id, "device_id": device.device_id, "email":device.owner}
        r = requests.post("http://tatatrent.embdev.in/mobile/devices/configure/", data=json.dumps(payload))
        print "Blinds triggered"

    message = 'I changed "%s" current state to "%s"!' %(device.device_name, action)
    client.publish("emb/iot/notifications/", "%s" %(message)) 
    print "message published", message
    return

    
handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'
def process_on_message(data):
    try:
        print 1, data
        ##refining data
        try:
            refined_data = data.rsplit(":")[-1]
            print refined_data.strip(), len(refined_data.strip())
            if len(refined_data.strip()) > 2 and refined_data.strip()[0] == '0':
                replace_data = refined_data.strip()[1:]
                if replace_data.startswith('0'):
                    replace_data = replace_data[1:]
                data = data.replace(refined_data.strip(), replace_data)
        except Exception, e:
            print "Error in refining", str(e)
        print 2, data    
        data = eval(str(data))
      
        print 2, data
        distance = ''
        if data["device_id"] == 'AutoCar':
            car_mode, drive_mode = get_autocar_mode()
            if data.has_key('distance'):
                distance = data['distance']
                if int(distance) < 2 or drive_mode== 'FOLLOW':
                    return
            command = data.get("command")
            if not command and car_mode == 'AUTO':
                if drive_mode == 'LANE':
                    command = 'stop'
                elif drive_mode == 'AVOID':
                    command = 'forward'
            if not command:
                return
            auto_car = AutoCar.objects.create(command=command)
            auto_car.speed = data.get("speed", 70)
            angle = int(data.get("angle", 0))
            if angle < 0:
                angle = 90-abs(angle)
            else:
                angle = 90 + abs(angle)

            auto_car.angle = angle
            if distance:
                auto_car.distance = distance
            auto_car.save()
            return

        action = data.get('ON / OFF', '')
        if not action:
            action = data.get('STATE', '')
        device = Devices.objects.filter(device_id=data["device_id"]).latest('id')
        device_properties = device.deviceproperties
        device_properties.current_state = action.upper()
        if data["device_id"] == 'EntryExit':
            device_properties.door_state= data.get('STATE', '').upper()
        elif data["device_id"] == 'BlindSlats':
            device_properties.blinds_state= data.get('BLINDS', '').upper()
            device_properties.slats_state= data.get('SLATS', '').upper()
        elif data["device_id"] == '0x0181CBBE':
            # Temperature sensor
            temperature = data['TEMPERATURE']
            device_properties.temperature = temperature
        device_properties.save()
        try:
            user = User.objects.get(email=device.owner)
        except Exception, e:
            user = ''
            print str(e)
        #TODO: open close states blinds states ??
        if data["device_id"] == '0x0181CBBE':
            device_data = DevicesData.objects.create(devices=device, action="TIME_INTERVAL", data=data['TEMPERATURE'])
        else:
            device_data = DevicesData.objects.create(devices=device, action=action.upper(), email="hardware kit")
        device_data.save()

        #This If condition is to turn lights to red in color symbolically emergency exit
        if device.device_id in ['SecurityAlarm', 'FireAlarm'] and user:
            try:
                if action.upper() == "ON":
                    event = UserEvents.objects.get(name='Fire Alarm')
                elif action.upper() == "OFF":
                    event = UserEvents.objects.get(name='Reset Alarm')
            except:
                event = ''
            if event:
                payload =  {"email": event.user.email, "event":event.id }
                r = requests.post(handle_events_url, data=json.dumps(payload))
                print "triggered", event.name
                result = True

        elif device.device_id in ["EntryExit"]:
            print "Im inside entry exit condition"
            try:
                if action.upper() == "OPEN":
                    event = UserEvents.objects.get(name='Deactivate Conference Hall')
                elif action.upper() == "CLOSE":
                    event = UserEvents.objects.get(name='Activate Conference Hall')
            except Exception, e:
                print str(e)
                event = ''
            if event:
                print 'Got the event', event.name
                payload =  {"email": event.user.email, "event":event.id }
                r = requests.post(handle_events_url, data=json.dumps(payload))
                print "triggered", event.name
                result = True
        elif "switch" in device.device_type.name:
            
            payload =  {"email": device.owner, "category":device.device_type.device_category.name, "device_id": data['device_id'], "ON / OFF": action.upper()}
            r = requests.post("http://tatatrent.embdev.in/mobile/devices/configure/", data=json.dumps(payload))
            result = True

    except Exception, e:
        print "Exception", str(e), data
        pass

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, obj, flags, rc):
    print("Connected with Result Code: "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, obj, msg):
    print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    if 'nlp' in msg.topic:
        process_voice_commands(msg.payload)
    else:
        process_on_message(msg.payload)

def on_publish(client, obj, mid):
    print("Publish mesage > mid: "+str(mid))

def on_subscribe(client, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(client, obj, level, string):
    print(string)

print "client created"
client = mqtt.Client('mqtt_server')
client.on_message = on_message
print "assigned on message"
client.on_connect = on_connect
print "assigned on connect"
client.on_publish = on_publish
print "assigned on publish"
client.on_subscribe = on_subscribe
print "assigned on subscribe"
client.connect("10.99.90.32", 1883, 3600)
print "client connected!!!!!!!!!!!!!!!"
client.subscribe("emb/iot/sensor")
print "Subscribed to gateway commands"

#TODO: under development
#Subscribe for remote control commands from mobile.
client.subscribe("emb/iot/autocar")
client.subscribe("emb/iot/nlp/")   # chat commands from user


#LOGIC FOR CONTINUOS PUBLISHING

def publish_messages():
    sent_time = 0
    def send_notification():
        msg = "Obstacles Ahead on the lane! You wanna take manual control??"
        payload = {"device_type": "autocar", "device_id":"AutoCar"}
        device = Devices.objects.filter(device_id='AutoCar')[0]
        mobile_device = User.objects.get(email=device.owner).gcm_device
        mobile_device.send_message(msg, extra=payload)
        print "Sent Push Notification"


    while True:
        car_mode, drive_mode = get_autocar_mode()
        time.sleep(0.3)
        try:
           socket_commands = SocketCommands.objects.all()
           if socket_commands:
               for socket_command in socket_commands:
                   message = socket_command.command
                   print message
                   #length = str(len(message))
                   #if len(length) == 1:
                   #    length = "000%s"%length
                   #elif len(length) == 2:
                   #    length = "00%s"%length
                   #elif len(length) == 3:
                   #    length = "0%s"%length
                   #client.publish("emb/iot/gateway/", "%s%s" %(length, message)) # requested not to send length
                   if socket_command.send_to:
                       print "to %s" %socket_command.publish_url
                       #client.publish("emb/iot/commands/%s/" %(socket_command.send_to), "%s" %(message))
                       client.publish(socket_command.publish_url, "%s" %(message))
                   else:
                       client.publish("emb/iot/gateway/", "%s" %(message)) 
                   socket_command.delete()
        except Exception, e:
            print "In Exception block", str(e)
            pass

        try:
            auto_car_commands = AutoCar.objects.filter(sent=False)
            for auto_car_command in auto_car_commands:
                if drive_mode != 'LANE':
                    message = '{"device_id":"AutoCar", "drive": "linedisable"}'
                    client.publish("emb/iot/iotcar/", "%s" %(message)) 


                message = ''
                direction = auto_car_command.command
                try: 
                    direction = re.findall("[a-zA-Z]+", direction)[0]
                except:
                    pass
                speed = auto_car_command.speed
                distance = auto_car_command.distance
                print "DISTANCEEEEEEEEEEEEEEEEEEEEEEEEE", distance, drive_mode, car_mode
                if distance and distance < 50 and car_mode == 'AUTO':
                    print "Im in if condition"
                    if drive_mode == 'AVOID':
                        direction = 'left'
                        message = '{"device_id":"AutoCar", "drive": "%s", "speed": %d}' %(direction.lower(), speed)
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                    elif drive_mode == 'LANE':
                        message = '{"device_id":"AutoCar", "drive": "linedisable", "speed":30, "distance":%s}' %distance
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                        message = '{"device_id":"AutoCar", "drive": "stop", "speed":30}'
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                        
                        if sent_time:
                            if time.time() - sent_time > 10:
                                send_notification()

                                sent_time = time.time()
                        else:
                            send_notification()
                            sent_time = time.time()
                elif distance and distance >= 50 and car_mode == 'AUTO':
                    print "its correct whats next"
                    if drive_mode == 'LANE':
                        message = '{"device_id":"AutoCar", "drive": "lineenable", "speed":20, "distance":%s}' %distance
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                    elif drive_mode == 'AVOID':
                        print "Im in elif condition >>>>>>>>>>>>>>>>>>>>>>>"
                        message = '{"device_id":"AutoCar", "drive": "forward", "speed":30}'
                        client.publish("emb/iot/iotcar/", "%s" %(message)) 
                elif car_mode == 'AUTO' and drive_mode == 'FOLLOW':
                    message = '{"device_id":"AutoCar", "drive": "%s", "speed": %d}' %(direction.lower(), speed)
                    client.publish("emb/iot/iotcar/", "%s" %(message)) 

                elif car_mode != 'AUTO':
                    print "Mannual commands here"
                    message = '{"device_id":"AutoCar", "drive": "%s", "speed": %d}' %(direction.lower(), speed)
                    client.publish("emb/iot/iotcar/", "%s" %(message)) 
                print "Auto Car command Published: ", message
                auto_car_command.sent = True
                auto_car_command.save()
                 
        except Exception, e:
            print "ERROR OCCURRED FROM AUTO CAR PUBLISHING", str(e)
 

t = threading.Thread(name='publish_messages', target=publish_messages)
t.start()


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
print "LOOP FOREVER"
client.loop_forever()
print "LOOP ENDED"
