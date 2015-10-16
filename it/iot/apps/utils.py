from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import  loader
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, AnonymousUser
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control

import json
from collections import OrderedDict

from iot.users.models import Devices, DevicesData, User, Applications

def details(request, DEVICE_CATEGORY=None, APP_TYPE=None):
    #Find stats in between dates also
    #data = DevicesData.objects.filter(devices__user=request.user)
    #devices = data.values_list('devices', flat='true').distinct()
    devices = Applications.objects.filter(devices__user=request.user, app_type=APP_TYPE).values_list('devices', flat='true')
    print ">?>>>>", devices

    result = []
    for device_id in devices:
        response = OrderedDict()
        device = Devices.objects.get(id=device_id)
        response['device'] = device
        device_data = DevicesData.objects.filter(devices=device)
        if device_data:
            #current_state = device_data.latest('id').action
            current_state = device.current_state
            light_on_data = device_data.filter(action="ON").order_by('id')
            print light_on_data
            light_off_data = device_data.filter(action="OFF").order_by('id')
            print light_off_data
            #CURRENT TEMPERATURE
            try:
                current_temperature = light_on_data.latest('id').data
            except:
                current_temperature ='' 
            try:
                latest_light_on = light_on_data.latest('id').created_date
            except:
                latest_light_on = ''
            try:
                latest_light_off = light_off_data.latest('id').created_date
            except:
                latest_light_off = ''

            light_on_dates = list(light_on_data.values_list('created_date', flat='true'))
            light_off_dates = list(light_off_data.values_list('created_date', flat='true'))
            light_on_count = light_on_data.count() 
            light_off_count = light_off_data.count() 
            print light_on_count , light_off_count

            if light_on_count == light_off_count:
                print "same length"
                pass
            elif light_on_count - 1 == light_off_count:   #Assuming currently in On State
                print "on -1 -== off"
                light_on_dates = light_on_dates[:-1]
            else:  
                print "came to else"
                #Some miss match b/w On and Off
                light_on_dates = []
                light_off_dates  = []
            cycles = zip(light_on_dates, light_off_dates)
            number_of_cycles = len(cycles)
  
            life_time = 0
            for cycle in cycles:
                cycle_diff = cycle[1] - cycle[0]
                life_time = life_time + cycle_diff.total_seconds()
        
        else:
            current_temperature = 'NA'
            current_state = "OFF"
            latest_light_on = 'NA'
            latest_light_off = 'NA'
            number_of_cycles = 'NA'
            life_time = 0
        response['Sensor Data'] = current_temperature
        response['Current State'] = current_state
        response['Latest Turned On at'] = latest_light_on
        response['Latest Turned Off at'] = latest_light_off
        response['Number Of Cycles'] = number_of_cycles      
        response['Life Time'] = "%.2f Hours" %(life_time / (60 * 60)) #In Hours

        result.append(response) 

    return result

def trigger(request, encoded_key1=None):
    device = Devices.objects.get(id=encoded_key1)
    device_properties = device.deviceproperties
    if device_properties.current_state == 'ON':
        device_properties.current_state = 'OFF'
    else:
        device_properties.current_state = 'ON'
    device_properties.save()


    d = DevicesData.objects.create(devices=device, action=device.current_state, email=request.user.email)
    d.save()
    return None

