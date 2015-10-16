#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python

import socket               # Import socket module
import threading
import time
import requests
import json

import sys, os
sys.path.append(os.path.abspath('..'))
sys.path.append('/var/www/www.embitel.com/it/iot')
sys.path.append('/var/www/www.embitel.com/it/')
import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")


import django
django.setup()

from iot.users.models import SocketCommands, DevicesData, Devices, User, UserEvents

from iot.views import send_push_notification

handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'
def connection_accept(c):
    while True:
        data = c.recv(1024)
        if not data:
            break
        print data
        try:
            data = eval(str(data))
            print data
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
            device_properties.save()
            try:
                user = User.objects.get(email=device.owner)
            except Exception, e:
                user = ''
                print str(e)
            #TODO: open close states blinds states ??
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
                try:
                    if action.upper() == "OPEN":
                        event = UserEvents.objects.get(name='Deactivate Conference Hall')
                    elif action.upper() == "CLOSE":
                        event = UserEvents.objects.get(name='Activate Conference Hall')
                except:
                    event = ''
                if event:
	            payload =  {"email": event.user.email, "event":event.id }
		    r = requests.post(handle_events_url, data=json.dumps(payload))
                    print "triggered", event.name
                    result = True
      
        except Exception, e:
            print "Exception", str(e)
            pass

        #c.send('Thank you for connecting')

if __name__ == "__main__":
    from iot.users.models import SocketCommands
    i=0
    while True:
        print i
        i = i+1
        try:
            c.close()
            s.close()
        except Exception, e:
            #remove this if its troubling
            try:
                c.close()
                s.close()
            except Exception, e:
                print "s.close and c,close in exception", str(e)
                pass

        try:
            print "opening new socket"
            s = socket.socket()         # Create a socket object
            host = '10.99.90.32'#socket.gethostname() # Get local machine name
            port = 5000                # Reserve a port for your service
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #To overcome ERROR IN BINDING [Errno 98] Address already in use
            s.bind((host, port))        # Bind to the port

            s.listen(5)                 # Now wait for client connection.
            c, addr = s.accept()     # Establish connection with client.
        except Exception, e:
            print "ERROR IN BINDING", str(e)
            time.sleep(5)
            continue

        def my_service():

            while True:
                try:
                   socket_commands = SocketCommands.objects.all()
                   if socket_commands:
                       for socket_command in socket_commands:
                           message = socket_command.command
                           length = str(len(message))
                           if len(length) == 1:
                               length = "000%s"%length
                           elif len(length) == 2:
                               length = "00%s"%length
                           elif len(length) == 3:
                               length = "0%s"%length

                           c.send("%s%s"%(length, message))
                           socket_command.delete()
                   time.sleep(5)
                except Exception, e:
                    print "In Exception block", str(e)
                    c.close()
                    break
                   

        t = threading.Thread(name='my_service', target=my_service)
        t.start()

        try:
            connection_accept(c)
        except:
            pass

