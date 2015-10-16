#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python
import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()

import json
import datetime
from collections import OrderedDict

from iot.users.models import Devices, DevicesData, User
from django.db import connection

def data_usage_graph(device, device_data_set, sc):
    dt = connection.ops.date_trunc_sql('day','created_date')

    response = []
    dates = list(device_data_set.filter(action__in = ["ON", "OFF"]).extra({'date':dt}).values_list('date', flat='true').distinct())
    dates.sort()
    #dates = SparkContext(dates)
    for date in dates:
        device_data = device_data_set.filter(created_date__startswith=str(date.date()))
        if device_data:
            device_on_data = device_data.filter(action="ON").order_by('id')
            device_off_data = device_data.filter(action="OFF").order_by('id')

            device_on_dates = list(device_on_data.values_list('created_date', flat='true'))
            device_off_dates = list(device_off_data.values_list('created_date', flat='true'))

            try:
                if device_data.order_by('id')[0].action == 'OFF':
                    device_on_dates = [date] + device_on_dates

                if device_data.order_by('-id')[0].action == 'ON':
                    print "Im here", date , datetime.timedelta(days=1)
                    if datetime.datetime.now() <= date + datetime.timedelta(days=1):
                        device_off_dates = device_off_dates + [datetime.datetime.now()]
                    else:
                        device_off_dates = device_off_dates + [date + datetime.timedelta(days=1)]

            except Exception, e:
                print str(e)
                pass

            device_on_dates  = sc.parallelize(device_on_dates)
            device_off_dates  = sc.parallelize(device_off_dates)

            device_on_count = device_on_dates.count()
            device_off_count = device_off_dates.count()

            if device_on_count == device_off_count:
                pass
            elif device_on_count - 1 == device_off_count:   #Assuming currently in On State
                device_on_dates = sc.parallelize(device_on_dates.collect()[:-1])
            else:
                #Some miss match b/w On and Off
                device_on_dates = []
                device_off_dates  = []
            cycles = device_on_dates.zip(device_off_dates)
            number_of_cycles = cycles.count()

            #accumulator for data usage per day
            life_time = sc.accumulator(0)
            print ">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>"
            cycles.foreach(lambda (x, y): life_time.add((y-x).total_seconds()))
            print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<"

        else:
            number_of_cycles = 0
            life_time = sc.accumulator(0)

        response.append(['%s'%str(date.date()), eval("%.2f" %(life_time.value / (60 * 60))), number_of_cycles]) #In Hours

    if response:
        response.insert(0, ["Device Usage", "Usage (in Hrs)", "Cycles"])

    return response



def details(request, device_key, source, sc):

    try:
        data = eval(str(request))
        source = 'mobile'
        monitor = data['monitor']
    except:
        data = request.POST.copy()


    device = Devices.objects.get(id=device_key)
    device_data_set = DevicesData.objects.filter(devices=device)

    if source and monitor == 'device_usage':
        data_usage_graph_values = data_usage_graph(device, device_data_set, sc)
        print data_usage_graph_values
        return data_usage_graph_values

def Devices_def(sc):
    devices = Devices.objects.all()#filter(device_type__name__contains='light')
    for device in devices:
        print sc
        request =  {'monitor': "device_usage"}
        data = details(request, device.id, None, sc)
        print data

