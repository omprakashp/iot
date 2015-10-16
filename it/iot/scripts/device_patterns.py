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

#CRITERIA
MIN_INPUT_DAYS = 45 #Not being used, ideally collect the latest 1 month or 2 months data
MIN_USAGE = 30 #Minimum device must be actived for X days (unique dates)
MIN_CRITERIA = 25 #To decide the device is active at nth hr every day - it has to satisfy TIMES >= MIN_USAGE / 2


#time slots for finding accuracy
time_slots = [0, 15, 30, 45]

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
    #conf = SparkConf().setAppName("IOT Testing App")
    #conf = conf.setMaster("local[*]")
    #sc   = SparkContext(conf=conf)
    users = User.objects.filter(email__startswith='madhujeet.tomar@embitel.com')
    for user in users:
        types = ['home_light', 'office_light', 'office_fan', 'home_fan', 'home_switch', 'office_switch', 'home_motion_detector', 'office_motion_detector']
        devices = Devices.objects.filter(device_type__name__in=types, owner=user.email)
        print "User: %s SUMMARY " %user.email
        for device in devices:
            response = reduce_algorithm(device, sc)

            print "Device Name: ", device.device_name
            if response:
                print "Pattern identified: This Device is regularly Turned ON at intervals ", response[0]
                print "Pattern identified: This Device is regularly Turned OFF at intervals", response[1]
            else:
                print "Data is Not enough to draw the pattern!"
    
            print "\n"
        

            try:
                if response[0] or response[1]:
                    device_pattern = DevicesPatterns.objects.get_or_create(devices=device)
                    device_pattern = DevicesPatterns.objects.get(devices=device)
                    if response[0]:
                        device_pattern.on_at =  response[0]
                    if response[1]:
                        device_pattern.off_at =  response[1]
                    device_pattern.save()
            except:
                pass 

        print "*********************"
        most_utilized_device_dict = find_most_utilized_device(sc, user.email)
        if most_utilized_device_dict:
            try:
                most_utilized_device = devices.get(id=most_utilized_device_dict['devices'])
                device_pattern = DevicesPatterns.objects.get_or_create(devices=most_utilized_device)
                device_pattern = DevicesPatterns.objects.get(devices=most_utilized_device)
                device_pattern.most_utilized_device = True
                device_pattern.save()
                print "Most utilized device is ", most_utilized_device.device_name
                print "Number of cycles so far ", most_utilized_device_dict['count']
            except Exception, e:
                print str(e)
                most_utilized_device = ''
        print "*********************\n"
