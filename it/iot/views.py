import os
import string
from random import choice
import re
#from django.template.loader import get_template
#from django.template import Context
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import datetime

from django.template import  loader
#from django.shortcuts import render_to_response
#from registration.models import Registration
from django.template import RequestContext
from django.shortcuts import render_to_response

import json
from django.views.decorators.csrf import csrf_exempt

import commands
from collections import OrderedDict
import datetime
import requests

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser

from forms import LoginForm, RegistrationForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control

from django.db import transaction
from iot.users.models import log_visit, User, Devices, Applications, DeviceProperties, DevicesData, Device_Type, Device_Category, UserEvents, DevicesPatterns, DevicesRules, SocketCommands, AutoCar
from push_notifications.models import GCMDevice, APNSDevice
from iot.mobile_utils import get_user_mobile_device
#to render the context instance to the template
#from django.template import *
#context_instance=RequestContext(request)


MOBILE_FLAG = False


'''
#logger setup
import glob
import logging
import logging.handlers

logger = logging.getLogger('kewl_actions.log')

LOGGER_PATH = '/var/log/nginx/kewl_actions.log'

hdlr = logging.FileHandler(LOGGER_PATH)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
'''


TESTING = True
MESSAGE_EXPIRY = 50

class InputDataException (Exception):
    def __init__ (self, str=None):
        self.error = str
        return

def reg_login(request):
    return render_to_response('login.html')

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def login_proc(request):

    try:
        data = eval(str(request.body))
        source = "mobile"
    except:
        #from web
        data = request.POST.copy()
        source = 'web'

    email = data['email']
    password = data['password']


    #logger.info("%s tried to login" %email)
    log_visit(request=request, action = 'LOGIN_TRY', email= email, source=source)

    if source == 'web':
        form_data = request.POST.copy()
    
        form = LoginForm(form_data)
        errors = form.errors
        if errors:
            return render_to_response('login.html', {'form': form})
        try:
            user = User.objects.get(email=email)
        except:
            return render_to_response('login.html', {'form': form})

    
    user = authenticate(username=email, password=password)
    if source == 'mobile':
        if user:
            auth_flag = True
            user = User.objects.get(email=email)
            if data.has_key('registration_id') and data['registration_id']:
                mobile_device = get_user_mobile_device(user)
                if not mobile_device:
                    mobile_type = data.get('mobile_type')
                    if mobile_type.lower == 'android':
                        mobile_device = GCMDevice.objects.create(registration_id=data['registration_id'])
                        mobile_device.save()
                        user.gcm_device = mobile_device
                        user.save()
                    elif mobile_type.lower == 'ios': 
                        mobile_device = APNSDevice.objects.create(registration_id=data['registration_id'])
                        mobile_device.save()
                        user.apns_device = mobile_device
                        user.save()
                else:
                    mobile_device.registration_id = data['registration_id']
                    mobile_device.save()
        else:
            auth_flag = False
        return HttpResponse(json.dumps({"auth": auth_flag}), content_type='application/json')
         
        
    login(request, user)
    #logger.info("%s (Kewl app management) Logged in successfully!" %email)
    log_visit(request=request, action = 'LOGGED_IN', email= email, source="WEB")
    response =  HttpResponseRedirect('/iot/dashboard/')
    
    #response.set_cookie("generate_token", True)
    return response

from django.contrib.auth import logout

def logout_view(request):
    try:
        #logger.info("%s Logged out!" %request.user.email)
        log_visit(request=request, action = 'LOG_OUT', email= request.user.email, source="WEB")
    except:
        pass
    logout(request)
    return HttpResponseRedirect('/login/')
    # Redirect to a success page.

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def register(request):

    form_data = request.POST.copy()
    
    form = RegistrationForm(form_data)
    errors = form.errors
    if errors:
        try:
            #logger.info("%s REGISTRATION FAILED !" %request.POST['register_email'])
            log_visit(request=request, action = 'REGISTRATION_FAILED', email= request.POST['register_email'], source="WEB")
        except:
            pass
        return render_to_response('login.html', {'form': form})

    # logout the existing user
    if (isinstance (request.user, AnonymousUser)):
        u = None
    else:
        u = request.user
        logout(request)

    email = request.POST['register_email']
    password = request.POST['register_password']

    try:
        u = User(username=email)
        u.set_password(password)
        u.email = email
        u.save()
        #logger.info("%s REGISTRATION SUCCESS !" %email)
        log_visit(request=request, action = 'REGISTRATION_SUCCESS', email= email, source="WEB")
    except Exception, e:
        return render_to_response('login.html', {'form': form})
    response = render_to_response('login.html', {'registration_status': "Registered successfully! Now you can login with your credentials!" })
    text = 'Hi,\n\nYou\'ve successfully registered with Embitel\'s Mobile Services!.\n\n If the registration hasn\'t done by you, please <a href="http://10.99.92.36:5000/unregister/%s/">click here</a> to restrict the access!\n\nRegards,\nEmbitel Mobility Team' %(u.id)
    #send_mail('donotreply@embitel.com', 'prakash.p@embitel.com', 'Registration Confirmation!', text, [], [])
    #TODO: email hardcoded
    return response

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def unregister(request, encoded_key1=None):
    
    try:
        user = User.objects.get(id=encoded_key1)
        user.delete()
    except Exception, e:
        pass
    response = render_to_response('unregister.html')
    return response

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def unregister(request, encoded_key1=None):
    
    try:
        user = User.objects.get(id=encoded_key1)
        user.delete()
    except Exception, e:
        pass
    response = render_to_response('unregister.html')
    return response

@csrf_exempt
def redirect_default_page(request):#, encoded_key1=None):
    
    if isinstance(request.user, AnonymousUser):
        return HttpResponseRedirect('/login/')
    return HttpResponseRedirect('/iot/dashboard/')


#TODO: UTILS
def get_iot_user(request):
    try:
        iot_user = User.objects.get(email=request.user.email)
    except:
        iot_user = None
    return iot_user

def clean_categories(request=None):
    categories = []
    for cat in get_device_categories():
        categories.append(cat.replace('_', ' '))
    return categories

def get_device_categories():
    categories = Device_Category.objects.all().values_list('name', flat='true')
    return categories
    
def get_categorywise_devices(category=None):
    if category:
        category = category.replace(' ', '_').lower()
        device_types = list(Device_Type.objects.filter(device_category__name=category).values_list('name', flat='true'))
        device_types = [dev.replace('_', ' ').title() for dev in device_types]
        return device_types
    result = {}
    categories = get_device_categories()
    for cat in categories:
        result[cat] = Device_Type.objects.filter(device_category__name=cat).values_list('name', flat='true')   

    return result
        

def get_features(device_type=None):
    if device_type:
        try:
            commands_dict = eval(Device_Type.objects.get(name=device_type).properties)
        except Exception, e:
            commands_dict = {}
        return commands_dict
    commands_dict = {}
    decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
    device_types = Device_Type.objects.all()
    for device_type in device_types:
        try:
            commands_dict[device_type.name] =  decoder.decode(str(device_type.properties)).keys()
        except:
            pass # features not defined
    return commands_dict


    
@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def dashboard(request):
    response = render_to_response('dashboard_home.html', {"title": "dashboard", "user": get_iot_user(request), "categories": get_device_categories()})
    return response

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def dashboard_proc(request):
    dob = request.POST.get('dob')
    first_name =  request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    iot_user = get_iot_user(request)
    if iot_user:
        if first_name:
            iot_user.first_name = first_name.strip()
        if last_name:
            iot_user.last_name = last_name.strip()
        try:
            iot_user.dob = datetime.datetime.strptime(dob, "%d-%m-%Y")
        except Exception, e:
            pass
        iot_user.save()
    response = render_to_response('dashboard_home.html', {"title": "dashboard", "data": "Profile Updated!", "user": get_iot_user(request)})
    return response
 

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def autocar(request):
    try:
        car_obj = AutoCar.objects.all().latest('id') 
        previous_obj =  AutoCar.objects.all().order_by('-id')[1]
        print car_obj
    except:
        car_obj = ''
        previous_obj = ''

    response = render_to_response('auto_car.html', {"command": car_obj.command, "speed": car_obj.speed, "angle": car_obj.angle, "previous_speed":previous_obj.speed, "previous_angle": previous_obj.angle} )
    return response

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def autocar_ajax(request):
    try:
        car_obj = AutoCar.objects.all().latest('id') 
    except:
        car_obj = ''

    result = {"updated_val": car_obj.angle, "updated_speed": car_obj.speed}
    print ">>>>>>>>>>>>>>>>>>>>>>>>>>>", result
    return HttpResponse(json.dumps(result), content_type='application/json')
 

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def device_details_display(request, device_key=None):
    try:
        device = Devices.objects.get(id=device_key)
    except:
        device = None

    response = render_to_response('device_details.html', {"device": device} )
    return response
 
@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def add_device(request):
    try:
        user = request.user
    except:
        return  HttpResponseRedirect('/logout/')

    response = render_to_response('add_device.html', {"title":"device_management", "categories" : get_device_categories(), "category_devices": get_categorywise_devices(), "device_types":get_features() })
    return response


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
#@login_required   #TODO: for mobile if logged in user works then no issues
@transaction.commit_on_success
def add_device_proc(request, source=None):
    try:
        user = request.user
    except:
        return  HttpResponseRedirect('/logout/')

    try:
        data = eval(str(request.body))
        source = "mobile"
    except:
        #from web
        data = request.POST.copy()
    try:
        device = Devices(device_id= data['device_id'])
        device.device_name = data['device_name']
        #if data['device_category']:
        #    device.device_category = data['device_category'].lower()
       
        device.manufacturer = data['manufacturer']
        if source:
            device_type = data['device_type'].replace(' ', '_').lower()
        else: #for web
            try:
                device_type = ''.join(list(set(data.getlist('device_type')) - set([''])))
            except:
                device_type = data["device_type"]
        device.device_type = Device_Type.objects.get(name=device_type)
        if data['warranty']:
            device.warranty = datetime.datetime.today() + datetime.timedelta(days=int(data['warranty'])*365)

        if data.has_key('gateway_ip') and data['gateway_ip']:
            device.gateway_ip = data['gateway_ip']

        if data.has_key('gateway_port') and data['gateway_port']:
            device.gateway_port = int(data['gateway_port'])

        device.save()
               
        if source:
            email = data['email'] #temp
            user = User.objects.get(email=email)
        else:    
            user = User.objects.get(email=request.user.email)
        device.owner = user.email
        device.user.add(user)
        device.save()

        try:
            device_properties = DeviceProperties(device=device)
            device_properties.save()
        except Exception, e:
            pass

        #map the device with its applications
        try:
            #TODO: try filter to get multiple apps
            application = Applications.objects.get(app_type__contains=device.device_type.name.rsplit('_')[-1])
            application.devices.add(device)
            application.save()
        except Exception, e:
            #if matching application is not there
            pass

    except Exception, e:
        raise

    if source:#mobile
        data['id'] = device.id
        return HttpResponse(json.dumps(data), content_type='application/json')
        
    return  HttpResponseRedirect('/iot/device_management/')



@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def delete_device(request, device_key):
    data =  request.POST.copy()
    device = ''
    try:
        pass #For demo purpose commented this delete devices
        #device = Devices.objects.get(owner=request.user.email, id=device_key)
        #device.delete()
    except:
        #Show form errors
        pass

    return  HttpResponseRedirect('/iot/device_management/')




def gateway_socket_communication(gateway_ip, gateway_port, data):
    import socket
    TCP_IP = gateway_ip
    TCP_PORT = gateway_port
    BUFFER_SIZE = 20
    MESSAGE = data
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    #data = s.recv(BUFFER_SIZE)
    s.close()

def send_push_notification(user, device=None):

    mobile_device = get_user_mobile_device(user)

    if not mobile_device:
        return

    payload = {"id":device.id, "device_id": device.device_id, "device_category":device.device_type.device_category.name, "device_type":device.device_type.name}#, "source": "mobile"}
    device_properties_dict =eval(device.device_type.properties)
    device_properties = device.deviceproperties
    for key, val in  device_properties_dict.iteritems():
        payload[key] = eval("device_properties.%s"%val)

    #DUMMY TRY EXCEPT BLOCK
    try:
        if payload.has_key('RGB_R'):
            payload["RGB"] = str(device_properties.rgb)
    except:
        pass

    ''' #COMMENTED GCM CODE
    try:
        if isinstance(mobile_device, APNSDevice):
            mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), badge=1, extra=payload)
        else:
            mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), extra=payload)
            #mobile_device.send_message(str(payload))
        print "SENT MESSAGE", "%s - Device configuration has been changed successfully!" %(device.device_name)
    except Exception, e:
        print "<>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<", str(e)
    '''
    return

def handle_mapped_devices(request, device):

    action = device.current_state
    mapped_devices = eval(device.mapped_devices)
    if mapped_devices:
        for mapped_device_id in mapped_devices:
            try:
                mapped_device = Devices.objects.get(id=mapped_device_id)
                if 'light' in mapped_device.device_type.name:
                    if action == mapped_device.current_state:
                        continue
                    else:
                        mapped_device_properties =  mapped_device.deviceproperties
                        mapped_device_properties.current_state = action
                        mapped_device_properties.save()
                        device_data = DevicesData.objects.create(devices=mapped_device, action=action, email="mapped_device")
                        device_data.save()
                elif 'blind' in mapped_device.device_type.name:
                    mapped_device_properties =  mapped_device.deviceproperties
                    if action == 'ON':
                        if mapped_device_properties.slats_state == 'OPEN':
                            continue
                        else:
                            mapped_device_properties.slats_state = 'OPEN' 
                    else:
                        if mapped_device_properties.slats_state == 'CLOSE':
                            continue
                        else:
                            mapped_device_properties.slats_state = 'CLOSE' 
                    mapped_device_properties.save()
 
                try:
                    user = User.objects.get(email=request.user.email)
                except:
                    user = User.objects.get(email=device.owner) #decide whether to send it to owner or any one else also M2M

                #send_push_notification(user, mapped_device) #COMMENTED GCM CODE
            except:
                pass   

    try:
        zigbee_devices = eval(device.mapped_devices)
        for zigbee_id in zigbee_devices:
            zigbee = Devices.objects.get(id=zigbee_id)
            #if zigbee.gateway_ip and zigbee.gateway_port:
            if 'light' in zigbee.device_type.name:
                message = json.dumps({"category": "my_office", "DIM": 100, "Current Color": zigbee.deviceproperties.rgb, "ON / OFF": zigbee.current_state, "device_category": "my_office", "device_type": "office_light", "id": zigbee.id, "device_id": zigbee.device_id})
            elif 'blind' in zigbee.device_type.name:
                message = json.dumps({"device_id": str(zigbee.device_id), "SLATS": str(zigbee.deviceproperties.slats_state)})
            sc = SocketCommands.objects.create()
            sc.command = str(message)
            sc.save()

            #gateway_socket_communication(zigbee.gateway_ip, zigbee.gateway_port, message)
    except Exception, e:
        print "Exception in handle mapped devices", str(e)
        #Catch Exception here and handle it 
        pass

    return


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def configure_device(request, device_key):
    result = OrderedDict()
    device = Devices.objects.get(id=device_key)
    features = get_features(device_type=device.device_type.name)
    features_dict = eval(str(device.device_type.properties))
    device_properties = device.deviceproperties
    for key, val in features_dict.iteritems():
        if key in ['RGB_R', 'RGB_G', 'RGB_B']:
            continue
        result[key] = eval("device_properties.%s" %val)
   
    users_accessible = list(device.user.exclude(email=request.user.email).values('email', 'id'))
    owner = device.owner 
 
    lights = list(Devices.objects.filter(owner=request.user.email, device_type__name__contains='light'))
    lights.extend(list(Devices.objects.filter(owner=request.user.email, device_type__name__contains='blind')))
    mapped_devices = eval(device.mapped_devices)

    response = render_to_response('configure_device.html', {"title":"device_management", "device_id": device.id, 'device': device, "lights": lights, "mapped_devices": mapped_devices,  "features": features, "categories": list(get_device_categories()), "features_dict": result, "users_accessible":users_accessible, "owner":owner, "user_profile":request.user, "modified_time": datetime.datetime.strftime(device.modified_date, "%d%m%Y%M%H%S")})
    return response

@csrf_exempt
#@cache_control(no_store=True, no_cache=True, must_revalidate=True,)         ???? CREATING ISSUES
#@login_required #TODO:
def configure_device_proc(request, device_key=None, source=None, event_data=None, publish=True):
    #from mobile {email, id, device_id, category}
    try:
        if event_data:
            data = event_data
        else:
            data = request.POST.copy()
        if device_key:
            device = Devices.objects.get(id=device_key)
        else:
            #if data is coming from any device
            device = Devices.objects.get(device_id=device_id)

        #TRY All the keys having on and off and assign on or off 
        try:
            #maintain in constants file
            #toggle_keys = ['ON / OFF', 'Engine Status', 'AC Status', 'Lights Status', 'Doors Status']
            toggle_keys = ['ON / OFF']
            data_keys  = data.keys()
            on_keys = list(set(data_keys).intersection(toggle_keys))
            for key in on_keys:
                data[key] = data[key].upper()

            off_keys = list(set(toggle_keys) - set((data_keys)))
            for key in off_keys:
                data[key] = "OFF"

        except Exception, e:
            pass

        if not data.has_key('ON / OFF'):
            data['ON / OFF'] = 'OFF'
        else:
            data['ON / OFF'] = data['ON / OFF'].upper()

    except:
        #from mobile
        data = eval(str(request.body).replace("\\", ''))
        source = 'mobile'
        try:
        #Hint: tr block is for mobile devices only
            device = Devices.objects.get(id=data["id"], device_type__device_category__name=data["category"].replace(' ', '_').lower(), user__email=data['email']) #TODO: authentication issue! please check for category and email, if the reuest is from mobile device
        except Exception, e:
            #This except block is for sensor devices
            print "Error from sensor part", str(e)
            device = Devices.objects.get(device_id=data["device_id"])
    keys = data.keys()
    device_type = device.device_type
    features = get_features(device_type=device.device_type.name)
    result = {}
    for key, val in features.iteritems():
        if key in keys:
            if key == 'Current Color':
               result['rgb_r'], result['rgb_g'], result['rgb_b']  = hex_to_rgb(data[key])
            result[val] = data[key]
    #TODO: write get_device_properties api
    device_properties = device.deviceproperties
    print "Can u here me ", features.values() 

    #if not device_properties:
    #    device_properties = DeviceProperties()
    #    device_properties.device = device
    #    device_properties.save()

    #TODO:This code is just to maintain blinds carefully. It will send commands if change in either blinds or slats
    if 'blind' in device.device_type.name:
        previous_states = {"BLINDS": device_properties.blinds_state, "SLATS": device_properties.slats_state}
    else:
       previous_states = {} 
              
    #device_properties = device.device_properties
    previous_state = device_properties.current_state
    device_properties.set_val(result)
    if "current_state" in features.values() and device_properties.current_state != previous_state:
        try:
            email = request.user.email
            if not email:
                email = device.user.email
        except:
            try:
                email = data['email']
            except:
                email = 'sensor'# device.user.email# TODO: Many to many relation will not result user email

        device_data = DevicesData.objects.create(devices=device, action=device_properties.current_state, email=email)
        device_data.save()

    elif data.has_key('TEMPERATURE'):
        device_data = DevicesData.objects.create(devices=device, action="TIME_INTERVAL", data=data['TEMPERATURE'])
        device_data.save()

    elif data.has_key('ZONE'):
        device_data = DevicesData.objects.create(devices=device, action="BEACON", data=data['ZONE'])
        device_data.save()
        #Zone based event activation from beacons 
        #TODO: inside config proc for beacon kills more memory and takes more time for beacon storage prefer unique view func
        zone =  int(data["ZONE"])
        handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'
        if zone == 1:
            try:
                if device_properties.zone_flag == False:  
                    event = UserEvents.objects.filter(name='Activate Conference Hall')[0]
                    payload =  {"email": device.owner, "event":event.id }
                    r = requests.post(handle_events_url, data=json.dumps(payload))
                    result = True
                    device_properties.zone_flag = True
                    device_properties.save()
            except Exception, e:
                result = False
        elif zone == 0:
            try:
                event = UserEvents.objects.filter(name='Deactivate Conference Hall')[0]
                payload =  {"email": device.owner, "event":event.id }
                r = requests.post(handle_events_url, data=json.dumps(payload))
                device_properties.zone_flag = False
                device_properties.save()
                result = True
            except Exception, e:
                result = False

    if not source:
        #send notification to mobile
        data['category'] = device.device_type.device_category.name
        data['device_id'] = device.device_id
        data['id'] = device.id
        try:
            user = User.objects.get(email=request.user.email)
        except:
            user = User.objects.get(email=device.owner) 
        mobile_device = get_user_mobile_device(user)
        try:
            payload = {"device_category":device.device_type.device_category.name, "device_type":device.device_type.name}
            for key, val in data.iteritems():
                if "RGB" in key:
                    continue
                if key in ["DIM"]:
                    val = int(val)
                payload[key] = val

            try:
                if payload.has_key('RGB_R'):
                    payload["RGB"] = str(device_properties.rgb)
            except:
                pass

            #To intimate mobile devices via mqtt #TODO:
            if "light" in device.device_type.name and publish:
                if event_data:
                    payload['device_id'] = 'G000'
                sc = SocketCommands.objects.create()
                sc.command = str(json.dumps(payload))
                if MOBILE_FLAG:
                    sc.publish_url = 'emb/iot/commands/%s/' %device.owner 
                    sc.send_to = user.email  #TODO: enable this if it has to work from mobile not from gateway
                sc.save()
            elif "fire_alarm" in device.device_type.name:
                sc = SocketCommands.objects.create()
                sc.command = str(json.dumps(payload))
                sc.publish_url = 'emb/iot/commands/%s/' %device.owner 
                sc.publish_url = 'emb/iot/fire_alarm/commands/%s/' %device.owner 
                sc.send_to = user.email  #TODO: enable this if it has to work from mobile not from gateway
                sc.save()

            #COMMENTED GCM CODE
            #print payload
            #if isinstance(mobile_device, APNSDevice):
            #    mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), badge=1, extra=payload)
            #else:
            #    mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), extra=payload)
            #    mobile_device.send_message(str(payload))
            #print "SENT MESSAGE", "%s - Device configuration has been changed successfully!" %(device.device_name)


        except Exception, e:
            print "<>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<", str(e)
 
    else:
        #TODO: REPEATED CODE FPR DEMO TO OPERATE FROM ONE MOBILE TO OTHER ! HERE SOURCE = MOBILE
        try:
            #TRY for mobile and except for sensors
            try:
                #user = User.objects.get(email=data['email'])
                user = User.objects.get(email=device.owner) 
            except:
                user = User.objects.get(email=device.owner) 
            mobile_device = get_user_mobile_device(user)
            if mobile_device: 
                try:
                    payload = {"device_category":device.device_type.device_category.name, "device_type":device.device_type.name}#{"source": "mobile"}
                    for key, val in data.iteritems():
                        if "RGB" in key:
                            continue
                        if key in ["id"]:
                            val = int(val)
                        payload[key] = val

                    try:
                        if data.has_key('RGB_R'):
                            payload["Current Color"] = str(device_properties.rgb)
                    except:
                        pass

                    #To intimate mobile devices via mqtt #TODO:
		    if "light" in device.device_type.name and publish:
			if event_data:
			    payload['device_id'] = 'G000'
			sc = SocketCommands.objects.create()
			sc.command = str(json.dumps(payload))
                        if MOBILE_FLAG:
			    sc.publish_url = 'emb/iot/commands/%s/' %device.owner 
			    sc.send_to = user.email  #TODO: enable this if it has to work from mobile not from gateway
			sc.save()
		    elif "fire_alarm" in device.device_type.name:
			sc = SocketCommands.objects.create()
			sc.command = str(json.dumps(payload))
			sc.publish_url = 'emb/iot/commands/%s/' %device.owner 
			sc.publish_url = 'emb/iot/fire_alarm/commands/%s/' %device.owner 
			sc.send_to = user.email  #TODO: enable this if it has to work from mobile not from gateway
			sc.save()


                    #CPMMENTED GCM CODE
                    #if isinstance(mobile_device, APNSDevice):
                    #    mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), badge=1, extra=payload)
                    #else:
                    #    mobile_device.send_message("%s - Configuration has been changed successfully!" %(device.device_name), extra=payload)
                    #print "SENT MESSAGE", "%s - Device configuration has been changed successfully!" %(device.device_name)
                except Exception, e:
                    print "<>>>>>>>>>>>>>>>>>>>>>>>>>>>><<<<<<<<<<<<", str(e)
        except:
            pass

    try:
        device = Devices.objects.get(id=device.id)
        device_properties = device.deviceproperties
    except Exception, e:
        print str(e)
        pass

    try:
        messages = []
        if device.gateway_ip and device.gateway_port:
            #TODO: create commands dynamicalluy
            if 'blind' in device.device_type.name :
                #if previous_states["BLINDS"] !=  device.deviceproperties.blinds_state:
                messages.append(json.dumps({"device_id": str(device.device_id), "BLINDS": str(device.deviceproperties.blinds_state)}))
                #if previous_states["SLATS"] !=  device.deviceproperties.slats_state:
                #    if device.deviceproperties.blinds_state == 'CLOSE':
                messages.append(json.dumps({"device_id": str(device.device_id), "SLATS": str(device.deviceproperties.slats_state)}))
            elif 'motion' in device.device_type.name:
                messages.append(json.dumps({"device_id": str(device.device_id), "STATE": str(device.deviceproperties.door_state)}))
            else:
                messages.append(json.dumps({"device_id": str(device.device_id), "ON / OFF": str(device.current_state)}))

            for message in messages:
                sc = SocketCommands.objects.create()
                sc.command = str(message)
                sc.save()
                #gateway_socket_communication(device.gateway_ip, device.gateway_port, message)
    except Exception, e:
        print str(e)
        #Handle exception here #TODO: if socket communication is failure dont update the elements to the database
        pass 

    handle_mapped_devices(request, device)
    if source:
        return HttpResponse(json.dumps({"success":True}), content_type='application/json')

    #response = render_to_response('configure_device.html', {"title":"device_management", "device": device, "features": features, "device_properties": device_properties, "categories": get_device_categories()})
    #return response
    if event_data:
        print "returning"
        return 1
    else:
        return  HttpResponseRedirect('/devices/configure/%s/' %device.id)
    

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def configure_device_add_user(request, device_key):
    data =  request.POST.copy()
    device = ''
    try:
        device = Devices.objects.get(owner=request.user.email, id=device_key)
        new_user = User.objects.get(email=data['email'])
        device.user.add(new_user)
        device.save()
    except:
        #Show form errors
        pass

    return  HttpResponseRedirect('/devices/configure/%s/' %device_key)


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def configure_device_delete_user(request, device_key, user_key):
    data =  request.POST.copy()
    device = ''
    try:
        device = Devices.objects.get(owner=request.user.email, id=device_key)
        delete_user = User.objects.get(id=user_key)
        device.user.remove(delete_user)
        device.save()
    except Exception, e:
        print str(e)
        #Show form errors
        pass

    return  HttpResponseRedirect('/devices/configure/%s/' %device_key)

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def configure_device_map_device(request, device_key):
    data =  request.POST.copy()
    device = ''
    try:
        device = Devices.objects.get(owner=request.user.email, id=device_key)
        if data.has_key('map_device_id'):
            requested_devices = data.getlist('map_device_id')
            requested_devices = [int(dev_id) for dev_id in requested_devices]
            device.mapped_devices = str(requested_devices)
            device.save()
        else: 
            device.mapped_devices = '[]'
            device.save()
           
    except Exception, e:
        print str(e)
        #Show form errors
        pass

    return  HttpResponseRedirect('/devices/configure/%s/' %device_key)

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
#@login_required
def my_events(request):


    try:
        data = eval(str(request.body))
        source = "mobile"
    except:
        #from web
        source = ''

    try:
        email = request.user.email
    except:
        email = data['email']

    user = User.objects.get(email=email)
    my_events = UserEvents.objects.filter(user=user).order_by('name')

    if source:
        my_events = list(my_events.values('name', 'id') )
        return HttpResponse(json.dumps(my_events), content_type='application/json')
    
    #overwriting my_events for web to show the scheduled timing to trigger event
    my_events = list(my_events.values('name', 'id', 'event_trigger_time', 'active') )

    from collections import defaultdict 
    devices = defaultdict(list)

    device_types = Device_Type.objects.all().order_by('name')

    device_types_dict = OrderedDict()
    for device_type in device_types:
        device_types_dict[device_type.id] = device_type.name

    for result in Devices.objects.filter(owner=request.user.email).exclude(device_type__name__icontains="head_unit").exclude(device_type__name__icontains="temperature").exclude(device_type__name__icontains="motion").exclude(device_type__name__icontains="cam").values('device_type', 'device_name', 'id').order_by('device_type', 'device_name'):
        devices[device_types_dict[result['device_type']]].append({"device_name":result['device_name'], "id":result['id']})    

    typewise_devices = dict(devices)


    response = render_to_response('my_events.html',{"typewise_devices": typewise_devices, "my_events": my_events})
    return response


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
#@login_required
def my_events_proc(request):
    try:
        data = eval(str(request.body))
        email = data['email']
        source = "mobile"
    except:
        #from web
        source = ''
        data = request.POST.copy()
        email = request.user.email

    try:
        device_ids = data.getlist('devices')
    except:
        device_ids = data['devices']

    try:
        if device_ids:
            if isinstance(eval(device_ids[0]), list):
                device_ids = eval(device_ids[0])
    except:
        pass
        
    if not source:
        device_dicts = {}
        for key, val in data.iteritems():
            try:
                dev_id, dev_property = key.split('_', 1)
                if dev_id not in device_ids:
                    continue
                if int(dev_id) in device_dicts.keys():
                    properties_dict = device_dicts[int(dev_id)]
                    properties_dict[dev_property] = val
                else:
                    properties_dict = {}
                    properties_dict[dev_property] = val
                    device_dicts[int(dev_id)] = properties_dict

            except:
                continue
    else:
        device_dicts = data['device_dicts']

    device_dicts_keys = device_dicts.keys()
    device_dicts_keys = [int(key) for key in device_dicts_keys]
    for device_id in device_ids:
        if int(device_id) in device_dicts_keys:
            continue
        else:
            device_dicts[int(device_id)] = {'ON / OFF': 'OFF'}

    #toggle_keys = ['ON / OFF', 'Engine Status', 'AC Status', 'Lights Status', 'Doors Status']
    toggle_keys = ['ON / OFF']
     
    event_dict = {}
    for device_id, device_data in device_dicts.iteritems():
        print device_id, device_data
        device = Devices.objects.get(id=device_id)
        
        device_type = device.device_type
        features = get_features(device_type=device.device_type.name)

        result = {}
        keys = device_data.keys()  
        for key, val in features.iteritems():
            if key in keys:
                print key, val
                try:
                    result[key] = device_data[key].upper()
                except:
                    result[key] = int(device_data[key]) # Remove int if its still creating problem
            else:
                if key in toggle_keys:
                    result[str(key)] = "OFF"
            if key == 'Current Color':
                print key, device_data
                result['RGB_R'], result['RGB_G'], result['RGB_B']  = hex_to_rgb(device_data[key])
                print result
  
        
        event_dict[device_id] = result




    if event_dict:
        user = User.objects.get(email=email)
        try:
            event = UserEvents.objects.get(user=user, name=data["event_name"]) 
            event.properties = str(event_dict)
        except:
            event = UserEvents.objects.create(user=user, name=data["event_name"], properties=str(event_dict)) 

        if data.has_key("hours") and data["hours"] and data.has_key("minutes") and data["minutes"]:
            hours = int(data['hours'])
            minutes = int(data['minutes'])
            event.event_trigger_time = str([hours, minutes])

        if data.has_key('active'):
            event.active = True
        else:
            event.active = False
        event.save() 

    if source:
        return HttpResponse(json.dumps({"success": True}), content_type='application/json')

    return  HttpResponseRedirect('/devices/my_events/')



@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
#@login_required
def handle_events(request, selected_event=None):

    try:
        print request.body
        data = eval(str(request.body))
        email = data['email']
        source = "mobile"
        selected_event = int(data["event"])
    except:
        #from web
        source = ''
        data = request.POST.copy()
        email = request.user.email

    user_event = UserEvents.objects.get(id=selected_event)

    if not user_event.active:
        #devices will be enabled if active flag is True
        return  HttpResponseRedirect('/devices/my_events/')
        

    event_properties = eval(user_event.properties)

    event_device_ids = event_properties.keys()
    lights_ids = Devices.objects.filter(device_type__name__icontains='light').values_list('id', flat='true')

    event_lights_count = 0
    event_lights_ids = []

    for dev_id in event_device_ids:
        if int(dev_id) in lights_ids:
            event_lights_count = event_lights_count + 1
            event_lights_ids.append(dev_id)

    #if event_lights_count > 2:
    #    for idx,dev_id in enumerate(event_lights_ids):
    #        if idx == 1:
    #            #FOR Group events sned one light command with G000 as device_id
    #            event_properties[dev_id]['device_id'] = 'G000' 
    #        else:
    #            event_properties.pop(dev_id, 0)

    publish_lights_message_count = 0
    for device_id, device_properties in event_properties.iteritems():
        publish = True        
        if event_lights_count > 2:
            try:
                if int(device_id) in lights_ids:
                    publish_lights_message_count = publish_lights_message_count + 1
                if publish_lights_message_count < 3:
                    publish = False
            except:
                pass
                
        result = configure_device_proc(request=request, device_key=device_id, source=None, event_data=device_properties, publish=publish)
        print "EVENT DEVICE ACTIVATION", result

    if source:
        return HttpResponse(json.dumps({"success": True}), content_type='application/json')
    return  HttpResponseRedirect('/devices/my_events/')


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def delete_event(request, event_id=None):

    print "ENTERED HERE"
    email = request.user.email

    user = User.objects.get(email=email)

    user_event = UserEvents.objects.get(id=event_id, user=user)

    #TODO:demo events
    demo_events = [21]
    if int(event_id) not in demo_events:
        user_event.delete()

    return  HttpResponseRedirect('/devices/my_events/')


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
#@login_required
def my_patterns(request):
    try:
        data = eval(str(request.body))
        source = "mobile"
    except:
        #from web
        source = ''

    try:
        email = request.user.email
    except:
        email = data['email']

    user = User.objects.get(email=email)
    devices_having_patterns = DevicesPatterns.objects.filter(devices__owner=email).order_by('id')
    device_patterns = []
    for pattern in devices_having_patterns:
        device_flag = False
        device_dict = OrderedDict()
        device_dict["device_details"] = [pattern.devices.device_name, pattern.devices.id]
        if eval(pattern.on_at):
            device_dict["On Patterns"] = eval(pattern.on_at)
            device_flag = True
        if eval(pattern.off_at):
            device_dict["Off Patterns"] = eval(pattern.off_at)
            device_flag = True

        if device_flag:
            device_patterns.append(device_dict)

    user_patterns = DevicesRules.objects.all().order_by('id')

    user_accepted_patterns = []
    for pattern in user_patterns:
        pattern_dict = OrderedDict()
        pattern_dict[pattern.id] = pattern.rule_name
        rules = eval(pattern.rules)
        print rules
        rules_list = []
        for device_id, device_properties in rules.iteritems():
            device_dict = OrderedDict()
            try:
                device = Devices.objects.get(id=device_id)
                device_dict[device.id] = device.device_name
            except:
                #Device doesnt exist or device deleted
                continue
            
            properties = device_properties['property'] 
            for index, prop in enumerate(properties):
                if prop == "current_state":
                    property_value  = device_properties['device_property_value'][index]
                    if property_value == "ON":
                        device_dict["On Patterns"] =  [tuple([int(timing.split(':')[0]), int(timing.split(':')[1])]) for timing in device_properties["pattern_timings"][index]]
                    elif property_value == "OFF":
                        device_dict["Off Patterns"] =  [tuple([int(timing.split(':')[0]), int(timing.split(':')[1])]) for timing in device_properties["pattern_timings"][index]]

            rules_list.append(device_dict)
        
        pattern_dict['rules'] = rules_list
        user_accepted_patterns.append(pattern_dict)
        
    print "User accepted patterns", user_accepted_patterns       
    response = render_to_response('my_rules.html', {"device_patterns": device_patterns, "user_accepted_patterns":user_accepted_patterns, "hrs_range": tuple([i for i in range(0,24)]), "mins_range":tuple([i for i in range(0,60)])})

    return response


@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def testing(request):
    #TODO: change the def name
    print request.POST
    data = request.POST
    keys = data.keys()
    pattern_keys =  [key for key in keys if "_pattern" in key]
    if not pattern_keys:
        return
    
    device_rules = DevicesRules.objects.create(rule_name=data['pattern_name'])
    pattern_dict = {}
    for pattern_key in pattern_keys:
        device_id, pattern_type = pattern_key.split("_", 1)
        try:
            device_patterns_object = DevicesPatterns.objects.get(devices_id=device_id)
        except Exception, e:
            print str(e)
        if not pattern_dict.has_key(device_id):
            print device_id, "if not"

            pattern_dict[device_id] = {}
            device_pattern_dict = pattern_dict[device_id]

            device_pattern_dict['property'] = []
            device_pattern_dict['device_property_value'] = []
            device_pattern_dict['pattern_timings'] = []
        
        device_pattern_dict = pattern_dict[device_id]
            
        device_property = 'current_state'
        pattern_timings = data.getlist(pattern_key)
        if "On " in pattern_type:
            device_property_value = 'ON'
            accepted_patterns = [tuple([int(str(pattern_timing).split(':')[0]), int(str(pattern_timing).split(':')[1])]) for pattern_timing in pattern_timings]
            recognized_on_at = list( set(eval(device_patterns_object.on_at)) - set(accepted_patterns) )
            print set(eval(device_patterns_object.on_at)), set(accepted_patterns)
            print "EARLIER", device_patterns_object.on_at
            device_patterns_object.on_at = recognized_on_at
            print "NOW", recognized_on_at

        elif "Off " in pattern_type:
            device_property_value = 'OFF'
            accepted_patterns = [tuple([int(str(pattern_timing).split(':')[0]), int(str(pattern_timing).split(':')[1])]) for pattern_timing in pattern_timings]
            recognized_off_at = list(set(eval(device_patterns_object.off_at)) - set(accepted_patterns))
            device_patterns_object.off_at = recognized_off_at
            print "EARLIER", device_patterns_object.off_at
            print "NOW", recognized_off_at
        device_pattern_dict['property'].append(device_property)
        device_pattern_dict['device_property_value'].append(device_property_value)
        device_pattern_dict['pattern_timings'].append(pattern_timings)
            
        device_patterns_object.save()

    print pattern_dict
    device_rules.rules = pattern_dict
    device_rules.save()
            
    return  HttpResponseRedirect('/devices/my_patterns/')



@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def device_management(request):
    devices = []
    user_devices = Devices.objects.filter(user=request.user).order_by('-created_date')#.values('device_name', 'device_id', 'device_category', 'manufacturer', 'warranty', 'created_date', 'modified_date')
    for user_device in user_devices:
        device_dict = OrderedDict()
        device_dict['device_key'] = user_device.id
        device_dict['Device Name'] = user_device.device_name
        device_dict['Device ID'] =  user_device.device_id
        device_dict['Category'] =  user_device.device_type.device_category.name.capitalize()
        device_dict['Manufacturer'] =  user_device.manufacturer
        device_dict['Warranty'] =  user_device.warranty
        device_dict['Created On'] =  user_device.created_date
        device_dict['Modified On'] =  user_device.modified_date
  
        device_dict['device_type'] =  user_device.device_type.name
        device_dict['device_name'] =  user_device.device_name
        devices.append(device_dict)


    device_patterns = DevicesPatterns.objects.all()
    pattern_text = ""
    for device_pattern in device_patterns:
        pattern_text += '''<ul><li><b><font color="green">%s</font></b><br/>''' %device_pattern.devices.device_name
        if device_pattern.on_at:
            pattern_text += "<b>-</b> Effectively turned ON at intervals: %s <br/>" %(', '.join(["%s:%s" %(i,j) for i, j in eval(device_pattern.on_at)]))
        if device_pattern.off_at:
            pattern_text += "<b>-</b> Effectively turned OFF at intervals: %s<br/>" %(', '.join(["%s:%s" %(i,j) for i, j in eval(device_pattern.off_at)]))
        if device_pattern.most_utilized_device:
            pattern_text += '''<p style="color:red"><b>-</b> Most utilized device of all your devices!</p></li></ul>'''
        else:
            pattern_text += "<br/></li></ul>"

    from django.utils.translation import ugettext as _
    response = render_to_response('device_management.html', {"title":"device_management", "devices": devices, "categories": get_device_categories(), "device_patterns": pattern_text})
    return response

##For Mobile Applications

@csrf_exempt
def save_mobile_device(request):
    from iot.mobile_utils import save_registration_id
    data = eval(str(request.body))
    user = User.objects.get(email=data['email'])
    user = save_registration_id(user=user, registration_id=data['registration_id'], mobile_type=data['mobile_device_type'])
    return HttpResponse(json.dumps({"success": True}), content_type='application/json')


@csrf_exempt
def AutoCar_mode(request):
    data = eval(str(request.body))
    user = User.objects.get(email=data['email'])
    device_id = "AutoCar"
    mode = data['mode']
    drive_mode = data.get('drive_mode', '')
    if drive_mode:
        drive_mode = drive_mode.upper()
   
    device = Devices.objects.filter(device_type__name__contains='autocar', device_id=device_id)[0]
    properties = device.deviceproperties
    properties.mode = mode.upper()
    if drive_mode:
        properties.drive_mode = drive_mode.upper()
    properties.save()
    return HttpResponse(json.dumps({"success": True}), content_type='application/json')

 
@csrf_exempt
def get_categories(request):
    data = eval(str(request.body))
    if not data:
        data = request.POST.copy()

    try:

        if data.has_key('get'):
            key = data['get']
        else:
            key = ''
        if key and key == 'categories':
            result = [CAT.capitalize() for CAT in clean_categories()]
            return HttpResponse(json.dumps(result), content_type='application/json')

        elif key and key == 'device_types':
            category = data['category']
            return HttpResponse(json.dumps(get_categorywise_devices(category)), content_type='application/json')

        else:
            return HttpResponse(json.dumps({}), content_type='application/json')
    except Exception, e:
        return HttpResponse(json.dumps({}), content_type='application/json')


@csrf_exempt
def get_registered_devices(request):
#{"warranty": "", "device_category": "automation", "device_name": "assadasOM", "device_type": "device_automation", "id": 63, "manufacturer": "Embitel", "email": "prakash.p@embitel.com", "device_id": "sadssaddssasadssad"}
    data = eval(str(request.body))
    category = data['category'].replace(' ', '_').lower()
    email = data['email']
    user = User.objects.get(email=email)
    devices = Devices.objects.filter(user=user, device_type__device_category__name=category)
    result = []
    for device in devices:
        device_dict = {'device_name': device.device_name, "device_id": device.device_id, "id": device.id, "device_category": device.device_type.device_category.name, "device_type": device.device_type.name}
        result.append(device_dict)
    
    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def get_device_details(request):
#{"warranty": "", "device_category": "automation", "device_name": "assadasOM", "device_type": "device_automation", "id": 63, "manufacturer": "Embitel", "email": "prakash.p@embitel.com", "device_id": "sadssaddssasadssad"}
    result = {}
    try:
        data = eval(str(request.body))
    except:
        data = request.POST.copy()    

    try:
        category = data['category'].replace(' ', "_").lower()
        email = data['email']
        device_id = data['device_id']
        user = User.objects.get(email=email)
        try:
            device = Devices.objects.get(user=user, device_type__device_category__name=category, id=data["id"], device_id=device_id)
        except Exception, e:
            print str(e)
            device = ''
    except:
        #If req is from sennsor devices
        device_id = data.get('device_id')
        try:
            device = Devices.objects.get(device_id=device_id)
        except:
            device = ''

    if device:
        #result = {'device_name': device.device_name, "device_id": device.device_id, "id": device.id, "device_category": device.device_category, "device_type": device.device_type }
        features_dict = get_features(device.device_type.name)
        device_properties = device.deviceproperties
        for key, val in features_dict.iteritems():
            if key and val:
                result[key] = eval("device_properties.%s" %val)


        try:
            if "RGB_R" in result.keys():
                result["RGB"] = str(device_properties.rgb)
        except:
            pass

    return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def get_devicetypes_and_devices(request):
    try:
        data = eval(str(request.body))
    except:
        data = request.POST.copy()    
    
    from collections import defaultdict
    devices = defaultdict(list)
    device_types = Device_Type.objects.all()

    device_types_dict = {}
    for device_type in device_types:
        device_types_dict[device_type.id] = device_type.name.replace('_', ' ').title()

    for result in Devices.objects.filter(owner=data['email']).exclude(device_type__name__icontains="head_unit").values('device_type', 'device_name', 'id').order_by('device_type', 'device_name'):
        devices[device_types_dict[result['device_type']]].append({"device_name":result['device_name'], "id":result['id']})

    typewise_devices = dict(devices)

    return HttpResponse(json.dumps(typewise_devices), content_type='application/json')


@csrf_exempt
def geo_fencing_action(request):
    result = []

    def turn_on_off_lights(devices, action):
        #TODO: For now only one device
        for device in devices:
            device_properties = device.deviceproperties
            if device_properties.current_state == action:
                continue

            device_properties.current_state = action
            device_properties.save()
            device_data = DevicesData.objects.create(devices=device, action=action, email=email)
            device_data.save()

        return device_properties

    try:
        data = eval(str(request.body).replace('true', 'True').replace('false', 'False'))
    except:
        data = request.POST.copy()

    email = data['email']
    
    # get all the home light devices
    devices = list(Devices.objects.filter(user__email=email, device_type__device_category__name='my_home', device_type__name__contains='light'))
    if not devices: 
        return HttpResponse(json.dumps({"success": True}), content_type='application/json')
    else:
        devices = devices[:1]
    location = eval(str(data['location']))
    if location:
        device_properties = turn_on_off_lights(devices, "ON")
    else:
        device_properties = turn_on_off_lights(devices, "OFF")

    user = User.objects.get(email=email)
    mobile_device = get_user_mobile_device(user)

    try:
        payload = {'category': 'my_home', 'DIM': device_properties.dim, 'ON / OFF': device_properties.current_state, 'id': devices[0].id, 'device_id': devices[0].device_id}
        if location:
            message = "Hello Buddy! Welcome to our sweet home!"
        else:
            message = "Bye Bye! See you soon! "
        #if isinstance(mobile_device, APNSDevice):              ##GCM PART COMENTED
        #    mobile_device.send_message(message, badge=1, extra=payload)
        #else:
        #    mobile_device.send_message(message, extra=payload)

    except Exception, e:
        print ">>>>", str(e)
        pass

    return HttpResponse(json.dumps({"success": True}), content_type='application/json')


@csrf_exempt
def configure_device_ajax(request):
    try:
        data = eval(str(request.body))
    except:
        data = request.POST.copy()

    modified_date = data['modified_time']
    device_id = data['device_id'] 

    try:
        device = Devices.objects.get(id=device_id)
        if datetime.datetime.strftime(device.modified_date, "%d%m%Y%M%H%S") == modified_date:
            result = 0
        else: 
            result = 1
    except Exception, e:
        device = ''
        result = 0
    if result and device:
        device_configuration = OrderedDict()
        features_dict = eval(device.device_type.properties)
        device_properties = device.deviceproperties
        for key, val in features_dict.iteritems():
            device_configuration[key] = eval("device_properties.%s" %val)

        inner_html = '''
                <table class="table table-striped table-hover">
                '''

        for feature, val in device_configuration.iteritems():
            if feature in ["RGB_R", "RGB_G", "RGB_B"]:
                continue
            inner_html =  inner_html + '''<tr>
                        <td align="right"> %s : </td> ''' %(feature)
            if val == "ON" or val == "OFF":
                inner_html = inner_html + '''<td align="center">
                                    <div class="onoffswitch" id="onoffswitch">'''
                if val == "ON":
                    inner_html = inner_html + '''<input type="checkbox" class="onoffswitch-checkbox" id="myonoffswitch%s" name="%s" checked>''' %(feature, feature)
                else:
                    inner_html = inner_html+ '''<input type="checkbox" class="onoffswitch-checkbox" id="myonoffswitch%s" name="%s">''' %(feature, feature)
                inner_html = inner_html +'''<label class="onoffswitch-label" id="label" for="myonoffswitch%s">
                                    <span class="onoffswitch-inner" id="inner"></span>
                                    <span class="onoffswitch-switch" id="switch"></span>
                                    </label>
                                    </div>
                       </td>'''%(feature)
            elif feature == "DIM":
                inner_html = inner_html + '''<td align="center">
                         <input type=range min=0 max=100 name="%s" value=%s id=fader step=1 onchange="outputUpdate(value)">
                         <output for=fader id=volume>%s</output> </td>''' %(feature, val, val)


            elif feature == "Current Color":
                inner_html = inner_html + '''<td align="left" style="text-align:center;color:%s;">
	             &#10074;&#10074;&#10074;&#10074;&#10074;&#10074;&#10074;&#10074;&#10074;&#10074;
        	     <label for="rgb"></label>
	             <input id="rgb" name="Current Color" type="color" value="%s"/>
        	     </td>'''%(val, val)


            else:
                inner_html = inner_html + '''<td align="center"> <input type="text" size="5" name="%s" value="%s"></td>'''%(feature, val)
                       

	    inner_html = inner_html + '''</tr>'''
        inner_html = inner_html + '''<tr><td/><td align="right">
                                <input style="background-color:#F29900" type="submit" value="Save">
                        </td>
                        </tr>
                        </table>
                         '''
        result = {"inner_html": inner_html, "mod_time": datetime.datetime.strftime(device.modified_date, "%d%m%Y%M%H%S")}
    return HttpResponse(json.dumps(result), content_type='application/json')


@csrf_exempt
def update_hardware_IP(request):
#{"warranty": "", "device_category": "automation", "device_name": "assadasOM", "device_type": "device_automation", "id": 63, "manufacturer": "Embitel", "email": "prakash.p@embitel.com", "device_id": "sadssaddssasadssad"}
    result = {}
    try:
        data = eval(str(request.body))
    except:
        data = request.POST.copy()

    
    return HttpResponse(json.dumps(data), content_type='application/json')

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def construction(request):

    response = render_to_response('construction.html', {})
    return response


#Webservice to handle Media Event
@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def media_event(request):
    
    data = eval(str(request.body).replace('true', 'True').replace('false', 'False'))
    media_state = data['media']
    handle_events_url = 'http://tatatrent.embdev.in/mobile/devices/handle_events/'
    if media_state:
        try:
            event = UserEvents.objects.filter(name='Movie Time')[0]
            payload =  {"email": data['email'], "event":event.id }
            r = requests.post(handle_events_url, data=json.dumps(payload))
            result = True
        except Exception, e:
            result = False
    else:
        try:
            event = UserEvents.objects.filter(name='Movie Break')[0]
            payload =  {"email": data['email'], "event":event.id }
            r = requests.post(handle_events_url, data=json.dumps(payload))
            result = True
        except Exception, e:
            result = False

    return HttpResponse(json.dumps({"success":result}), content_type='application/json')


