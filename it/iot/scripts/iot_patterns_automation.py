import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()

from iot.users.models import DevicesRules, Devices
import datetime
import random
import requests
import json

configure_url = 'http://tatatrent.embdev.in/mobile/devices/configure/'

now = datetime.datetime.now()
time = "%s:%s" %(int(now.hour), int(now.minute))

patterns = DevicesRules.objects.filter(rules__contains=time)
print patterns
if not patterns:
    sys.exit()

for pattern in patterns:
    rules = eval(pattern.rules)
    for key, val in rules.iteritems():
        if not time in str(val):
            continue
        try:
            device = Devices.objects.get(id=key)
            pattern_timings = val['pattern_timings']
            device_property_value = val['device_property_value']
            i = 0 #to find the index of property and value for device
            for pattern_list in pattern_timings:
                if time in pattern_list:
                    payload = {"ON / OFF": device_property_value[i]}
                    payload['email'] = device.owner
                    payload['device_id'] = device.device_id
                    payload['id'] = str(device.id)
                    payload['category'] = str(device.device_type.device_category.name)
                    r = requests.post(configure_url, data=json.dumps(payload))

                i = i+1
        except Exception, e:
            print str(e)
            continue

