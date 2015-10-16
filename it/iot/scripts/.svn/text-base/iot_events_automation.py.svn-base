import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()

from iot.users.models import UserEvents
import datetime
import random
import requests
import json

now = datetime.datetime.now()
hrs, mins = now.hour, now.minute
print hrs, mins
handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'
events = UserEvents.objects.filter(event_trigger_time=str([hrs, mins]), active=True)
for event in events:
    try:
        payload =  {"email": event.user.email, "event":event.id }
        r = requests.post(handle_events_url, data=json.dumps(payload))
        result = True
    except Exception, e:
        print str(e)
        result = False
    print "Event Triggered", event.name




