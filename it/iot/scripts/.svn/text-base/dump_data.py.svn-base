import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()

from iot.users.models import Devices, DevicesData
import datetime
import random

devices = list(Devices.objects.filter(device_type__name__in=['home_light', 'office_light', 'office_fan', 'home_fan', 'home_switch', 'office_switch', 'home_motion_detector', 'office_motion_detector'], owner='prakash.p@embitel.com'))

on_hrs = [3, 8, 11]
off_hrs = [2, 9, 12]

for device in devices:
    on_hrs = [i+1 for i in on_hrs]
    off_hrs = [i+1 for i in on_hrs]

    queries = []
    date = datetime.datetime.today() - datetime.timedelta(days=30)
    while date <= datetime.datetime.today():
        date = date + datetime.timedelta(days=1)
        for on_hr in on_hrs:
            random_mins = random.randint(10, 50) 
            action = 'ON'
            date = datetime.datetime(date.year, date.month, date.day, on_hr, random_mins, 50)
            d = DevicesData(devices=device, email=device.owner, created_date=date, action = action)
            queries.append(d)

        for off_hr in off_hrs:
            random_mins = random.randint(10, 50) 
            action = 'OFF'
            date = datetime.datetime(date.year, date.month, date.day, off_hr, random_mins, 50)
            d = DevicesData(devices=device, email=device.owner, created_date=date, action = action)
            queries.append(d)

    print "LEN", len(queries)
    print "Bulk Insert started"
    DevicesData.objects.bulk_create(queries)
    print "Bulk Insert Done!"

