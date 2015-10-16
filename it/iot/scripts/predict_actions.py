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
from iot.users.models import Devices, DevicesData, User, DevicesPatterns
from django.db import connection
from django.db.models import Count

from operator import add
from pyspark import SparkContext

import datetime
from collections import OrderedDict


'''
Assumptions
Minimum number of records should be atleast 15 days records - unique on dates should be >15
'''


def reduce_algorithm(device, sc):

    #Consider only latest one or 2 months of data
    device_data = list(DevicesData.objects.filter(devices=device, action__in=['ON', 'OFF']).filter(created_date__gte=datetime.datetime.now()-datetime.timedelta(days=45)).values('action', 'created_date'))
    if not device_data:
        return
    device_data = sc.parallelize(device_data)

    #action_on_data = device_data.filter(lambda x: x['action']=='ON').map(lambda x: x['created_date'])
    #action_off_data = device_data.filter(lambda x: x['action']=='OFF').map(lambda x: x['created_date'])

    #unique_on_dates = action_on_data.map(lambda x: x.date()).distinct()
    #unique_off_dates = action_off_data.map(lambda x: x.date()).distinct()


    #To find accuracy including minutes, storing data with minutes
    action_on_data_till_mins = device_data.filter(lambda x: x['action']=='ON').map(lambda x: datetime.datetime(x['created_date'].year, x['created_date'].month, x['created_date'].day, x['created_date'].hour, x['created_date'].minute))
    action_off_data_till_mins = device_data.filter(lambda x: x['action']=='OFF').map(lambda x: datetime.datetime(x['created_date'].year, x['created_date'].month, x['created_date'].day, x['created_date'].hour, x['created_date'].minute))


    action_on_data_till_hrs = action_on_data_till_mins.map(lambda x: datetime.datetime(x.year, x.month, x.day, x.hour))
    action_off_data_till_hrs = action_off_data_till_mins.map(lambda x: datetime.datetime(x.year, x.month, x.day, x.hour))



    #print "Number of records available for action ON:  ",action_on_data.count() 
    #print "Number of records available for action OFF: ",action_off_data.count() 

    #Unique on times are derived from below but not dates
    unique_on_dates_till_hrs = action_on_data_till_hrs.distinct()
    unique_off_dates_till_hrs = action_off_data_till_hrs.distinct()

    #Unique on dates are derived 
    #print unique_on_dates_till_hrs.map(lambda x: x.date()).distinct().collect()
    number_of_days_on = unique_on_dates_till_hrs.map(lambda x: x.date()).distinct().count()
    number_of_days_off = unique_off_dates_till_hrs.map(lambda x: x.date()).distinct().count()
    #print "Number of days device used", number_of_days_on
    if number_of_days_on < MIN_USAGE: #Minimum of 20 days the device should be in use
        return

    try:
        draw_pattern_ON = unique_on_dates_till_hrs.map(lambda x: (x.hour,1)).reduceByKey(add).sortBy(lambda x: x[1])
        draw_pattern_OFF = unique_off_dates_till_hrs.map(lambda x: (x.hour,1)).reduceByKey(add).sortBy(lambda x: x[1])
        draw_pattern_ON_qualified = draw_pattern_ON.filter(lambda x: x[1] > MIN_CRITERIA).collect()
        draw_pattern_OFF_qualified = draw_pattern_OFF.filter(lambda x: x[1] > MIN_CRITERIA).collect()
        #print "patterns", draw_pattern.collect()
        if not draw_pattern_ON_qualified:
            return
        ON_SUMMARY = []
        for qualified_pattern in draw_pattern_ON_qualified:
            max_hr_ON = qualified_pattern[0] #draw_pattern_ON = [(hour, times), (hour, times), ---]

            def accurate_time(date_time):
                return min(time_slots, key=lambda x:abs(x-date_time.minute))

            try:
                ON_measure_accuracy_till_mins = action_on_data_till_mins.filter(lambda x: x.hour == max_hr_ON).map(lambda x: (accurate_time(x), 1)).reduceByKey(add).sortBy(lambda x: x[1]).collect()
                ON_accuracy_at_mins = ON_measure_accuracy_till_mins[-1][0] #results at which minute its max
                ON_SUMMARY.append((max_hr_ON, ON_accuracy_at_mins))
            except Exception, e:
                ON_SUMMARY.append((max_hr_ON, 0))
                print "Exception while calculating accuracy including MINS ONN", str(e)
                accuracy_at_mins = ''

        OFF_SUMMARY = []
        for qualified_pattern in draw_pattern_OFF_qualified:
            max_hr_OFF = qualified_pattern[0] #draw_pattern_ON = [(hour, times), (hour, times), ---]

            def accurate_time(date_time):
                return min(time_slots, key=lambda x:abs(x-date_time.minute))

            try:
                OFF_measure_accuracy_till_mins = action_off_data_till_mins.filter(lambda x: x.hour == max_hr_OFF).map(lambda x: (accurate_time(x), 1)).reduceByKey(add).sortBy(lambda x: x[1]).collect()
                OFF_accuracy_at_mins = OFF_measure_accuracy_till_mins[-1][0] #results at which minute its max
                OFF_SUMMARY.append((max_hr_OFF, OFF_accuracy_at_mins))
            except Exception, e:
                OFF_SUMMARY.append((max_hr_OFF, 0))
                print "Exception while calculating accuracy including MINS OFFF", str(e)
                accuracy_at_mins = ''

        ON_SUMMARY.sort()
        OFF_SUMMARY.sort()
 
        return ON_SUMMARY, OFF_SUMMARY

    except Exception, e:
        print str(e)
        return

def find_most_utilized_device(sc, email):
    devices_data = list(DevicesData.objects.filter(action='ON', devices__owner=email).values('devices').annotate(count=Count('devices')))
    if not devices_data:
        return
    devices_data = sc.parallelize(devices_data)
    most_utilized_device = devices_data.max(key=lambda x: x['count'])
    return most_utilized_device

if __name__ == "__main__":

    
    sc = SparkContext(appName="IOT Testing App")
    users = User.objects.filter(email='madhujeet.tomar@embitel.com')
    for user in users:
        devices_data = DevicesData.objects.filter(devices__owner=user.email, created_date__gte=(datetime.datetime.now()-datetime.timedelta(days=2)).date).order_by('id')
        actions = list(devices_data.values('devices', 'action', 'created_date'))
        datewise_actions = {}
        for action in actions:
            action_date = action['created_date']
            action_date = action_date.date()
            if action_date in datewise_actions.keys():
                datewise_actions[action_date].append((action['devices'], action['action']))
            else:
                datewise_actions[action_date] = [(action['devices'], action['action'])]

        print datewise_actions 
            
