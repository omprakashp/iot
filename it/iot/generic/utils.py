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
from iot.mobile_utils import get_user_mobile_device
from push_notifications.models import APNSDevice, GCMDevice

def details(request, DEVICE_CATEGORY=None, APP_TYPE=None):
    #Find stats in between dates also
    #data = DevicesData.objects.filter(devices__user=request.user)
    #devices = data.values_list('devices', flat='true').distinct()
    #category_devices = Devices.objects.filter(user=request.user, device_type__device_category__name=DEVICE_CATEGORY)
    devices = Devices.objects.filter(user=request.user, device_type__device_category__name=DEVICE_CATEGORY).values_list('id', flat='true')
    #devices = Applications.objects.filter(devices__in=category_devices).values_list('devices', flat='true')
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
            device_on_data = device_data.filter(action="ON").order_by('id')
            device_off_data = device_data.filter(action="OFF").order_by('id')
            #CURRENT TEMPERATURE
            try:
                latest_device_on = device_on_data.latest('id').created_date
            except:
                latest_device_on = ''
            try:
                latest_device_off = device_off_data.latest('id').created_date
            except:
                latest_device_off = ''

            device_on_dates = list(device_on_data.values_list('created_date', flat='true'))
            device_off_dates = list(device_off_data.values_list('created_date', flat='true'))
            device_on_count = device_on_data.count() 
            device_off_count = device_off_data.count() 
            print device_on_count , device_off_count

            if device_on_count == device_off_count:
                print "same length"
                pass
            elif device_on_count - 1 == device_off_count:   #Assuming currently in On State
                print "on -1 -== off"
                device_on_dates = device_on_dates[:-1]
            else:  
                print "came to else"
                #Some miss match b/w On and Off
                device_on_dates = []
                device_off_dates  = []
            cycles = zip(device_on_dates, device_off_dates)
            number_of_cycles = len(cycles)
  
            life_time = 0
            for cycle in cycles:
                cycle_diff = cycle[1] - cycle[0]
                life_time = life_time + cycle_diff.total_seconds()

            try:
                current_device_data = device_on_data.latest('id').data
            except:
                current_device_data ='' 

        
        else:
            current_device_data = 'NA'
            current_state = "OFF"
            latest_device_on = 'NA'
            latest_device_off = 'NA'
            number_of_cycles = 'NA'
            life_time = 0

        #Made this as generic how to show what toshow based on device type

        response['Device Data'] = current_device_data
        response['Current State'] = current_state
        response['Latest Turned On at'] = latest_device_on
        response['Latest Turned Off at'] = latest_device_off
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

    #TODO: for many to many relation manager device.user wont work
    try:
        data = request.POST.copy()
        data['category'] = device.device_type.device_category.name
        data['device_id'] = device.device_id
        data['id'] = device.id
  
        payload = {}
        for key, val in data.iteritems():
            payload[key] = val

        user = User.objects.get(email = request.user.email)
        mobile_device = get_user_mobile_device(user)
        if isinstance(mobile_device, APNSDevice):
            mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), badge=1, extra=payload)
            print "SENT MESSAGE", payload
        elif isinstance(mobile_device, GCMDevice):
            mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), extra=payload)
            print  "SENT MESSAGE ANDROID"
        else:
            pass
    except Exception, e:
        print "Error in push notifications", str(e)


    d = DevicesData.objects.create(devices=device, action=device.current_state, email=request.user.email)
    d.save()
    return device.device_type.device_category.name

