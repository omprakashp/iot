from django.template.defaulttags import register
from iot.constants import get_features
from iot.users.models import UserEvents
from iot.users.models import Devices
from collections import OrderedDict

"""
@register.filter
def get_item(dictionary, key):
    print dictionary, key, dictionary.get(key)
    return dictionary.get(key)
"""

@register.filter(name='lookup')
def cut(value, arg):
    print value
    print arg
    return value[arg]

@register.filter(name='clean_title')
def cut(value):
    if isinstance(value, (str, unicode)):
        return value.replace('_', ' ')
    else:
        print value, type(value)
        return value

@register.filter(name='pass_keys')
def pass_keys(value):
    if value in ["device_key", "device_type", "device_name"]:
        return True
    else:
        return False 

@register.filter(name='get_features_dict')
def get_features_dict(device):
    import json
    result = []
    device = Devices.objects.get(id=device['id'])
    #decoder = json.JSONDecoder(object_pairs_hook=OrderedDict)
    #features_dict = decoder.decode(str(device.device_type.properties))
    features_dict = eval(device.device_type.properties)
    for key, val in features_dict.iteritems():
        if key in ['RGB_R', 'RGB_G', 'RGB_B']:
            continue
        else:
            result.append(key)
    return result



@register.filter(name='get_event_properties')
def get_event_properties(event_id, dev_id=None):
    event = UserEvents.objects.get(id=event_id)
    event_properties = eval(event.properties)
    result = []
    for device_id, device_properties in event_properties.iteritems():
        if dev_id:
            if not dev_id == device_id:
                continue
        
        device = Devices.objects.get(id=device_id)
        device_result_dict = OrderedDict()
        device_result_dict["Device Name"] =  device.device_name
        device_features = eval(device.device_type.properties)
        device_properties_keys = device_properties.keys()
        for property_name, db_property_name in device_features.iteritems():
            if property_name in ["RGB_R", "RGB_G", "RGB_B"]:
                continue
            if property_name in  device_properties_keys:
                device_result_dict[property_name] = device_properties[property_name]
        
        if dev_id: 
             return [[dev_id, device_result_dict]]
        result.append([device_id, device_result_dict])

    print result
    return result


@register.filter(name='get_event_devices')
def get_event_devices(event_id, req_type=None):
    event = UserEvents.objects.get(id=event_id)
    event_properties = eval(event.properties)
    devices = event_properties.keys()
    if req_type:
        print devices
        return devices
    devices = [str(device_id) for device_id in devices]
    return devices

@register.filter(name='get_time')
def get_time(time_type):
    if time_type == 'hours':
        return [i for i in range(0, 24)]
    elif time_type == 'minutes':
        return [i for i in range(0, 60)]

@register.filter(name='get_event_time')
def get_event_time(event_time, req=None):
    event_time = eval(event_time)
    if req == 'hours':
        return int(event_time[0])
    else:
        return int(event_time[1])

