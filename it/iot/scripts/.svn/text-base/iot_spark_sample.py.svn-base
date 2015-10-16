#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python
import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()


from operator import add

from pyspark import SparkContext

import json
import datetime
from collections import OrderedDict

from iot.users.models import Devices, DevicesData, User




def data_usage_graph(device, device_data_set):
    from django.db import connection
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
                    if datetime.datetime.now() <= date + datetime.timedelta(days=1):
                        device_off_dates = device_off_dates + [datetime.datetime.now()]
                    else:
                        device_off_dates = device_off_dates + [date + datetime.timedelta(days=1)]

            except Exception, e:
                print str(e)
                pass

            device_on_count = len(device_on_dates)
            device_off_count = len(device_off_dates)


            if device_on_count == device_off_count:
                pass
            elif device_on_count - 1 == device_off_count:   #Assuming currently in On State
                device_on_dates = device_on_dates[:-1]
            else:
                #Some miss match b/w On and Off
                device_on_dates = []
                device_off_dates  = []
            cycles = zip(device_on_dates, device_off_dates)
            number_of_cycles = len(cycles)
            life_time = 0
            for cycle in cycles:
                cycle_diff = cycle[1] - cycle[0]
                life_time = life_time + cycle_diff.total_seconds()

        else:
            number_of_cycles = 0
            life_time = 0


        response.append(['%s'%str(date.date()), eval("%.2f" %(life_time / (60 * 60))), number_of_cycles]) #In Hours

    if response:
        response.insert(0, ["Device Usage", "Usage (in Hrs)", "Cycles"])

    return response



def time_interval_graph(device=None, device_data_set=None, source=None):
    time_intervals = []
    device_data = device_data_set.filter(action__in=["ON", "OFF"]).order_by('id').values('created_date', 'action')
    import datetime, calendar
    counter = 0
    if 'temperature' in device.device_type.name:
        time_intervals = []
        device_data = device_data_set.order_by('id').values('created_date', 'data')
        counter = 0
        opp_temperature = 0
        for data in device_data:
            created_date = data['created_date']
            created_date_in_ms = calendar.timegm(created_date.utctimetuple())*1000.0 + created_date.microsecond * 0.0011383651000000
            if source:
                created_date_in_ms = str(created_date).split('.')[0]
            if not data['data']:
                continue
            temperature = float(data['data'])
            if counter != 0:
                time_intervals.append([created_date_in_ms, opp_temperature])
            time_intervals.append([created_date_in_ms, temperature])
            try:
                opp_temperature = float(data['data'])
            except Exception, e:
                print str(e)
            counter = counter + 1
        return time_intervals

    #IF NOT TEMPERATURE
    counter = 0
    for data in device_data:

        if data['action'] == 'ON':
            action = 1
            opp_action = 0
        else:
            action = 0
            opp_action = 1
        created_date = data['created_date']
        created_date_in_ms = calendar.timegm(created_date.utctimetuple())*1000.0 + created_date.microsecond * 0.0011383651000000
        if source:
            created_date_in_ms = str(created_date).split('.')[0]

        counter = counter + 1
        if counter != 0:
            time_intervals.append([created_date_in_ms, opp_action])
        time_intervals.append([created_date_in_ms, action])

    return time_intervals

#LIGHT
def details(request, device_key, source):

    try:
        data = eval(str(request))
        source = 'mobile'
        monitor = data['monitor']
    except:
        data = request.POST.copy()


    device = Devices.objects.get(id=device_key)
    #result = []
    device_data_set = DevicesData.objects.filter(devices=device)

    if source and monitor == 'device_usage':
        data_usage_graph_values = data_usage_graph(device, device_data_set)
        return data_usage_graph_values

    elif source and  monitor == 'time_interval':
        time_interval_graph_values = time_interval_graph(device, device_data_set, source)
        return time_interval_graph_values

    elif source:
        return []

    #DATA USAGE GRAPH:
    data_usage_graph_values = data_usage_graph(device, device_data_set)
    #TIME INTERVAL GRAPH
    time_interval_graph_values = time_interval_graph(device, device_data_set)


    return data_usage_graph_values, time_interval_graph_values




if __name__ == "__main__":


    #sc = SparkContext(appName="IOT Testing App")

    #print dir(sc)
    devices = Devices.objects.filter(id=18)
    for device in devices:
        print "\n\nDevice", device.id, device.device_name
        request =  {'monitor': "device_usage"}

        data = details(request, device.id, None)
        print "FINAL DATA", data

    '''

    lines = sc.parallelize(data)

    counts = lines.flatMap(lambda x: x.split(' ')) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)
    output = counts.collect()
    write = ''
    for (word, count) in output:
        try:
            print "%s: %i" % (word, count)
            write += '\n'+ "%s: %i" % (word, count)
        except:
            pass

    import time
    time.sleep(10)
    '''

    #sc.stop()


