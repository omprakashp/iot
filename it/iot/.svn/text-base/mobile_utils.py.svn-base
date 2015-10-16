from push_notifications.models import APNSDevice, GCMDevice

def get_model(device_type=None):
    if device_type == 'ios':
        return APNSDevice
    elif device_type == 'android':
        return GCMDevice
    else:
        return None

def save_mobile_device(user=None, mobile_device=None):
    if isinstance(mobile_device, APNSDevice):
        user.apns_mobile_device = mobile_device
    
    elif isinstance(mobile_device, GCMDevice):
        user.gcm_mobile_device= mobile_device

    user.save()
    return user

def save_registration_id(user=None, registration_id=None, mobile_device_type=None):
    model = get_model(mobile_device_type)
    try:
        mobile_device = APNSDevice.objects.get(registration_id=registration_id)
    except:
        mobile_device = model.objects.create(registration_id=registration_id)
        mobile_device.save()

    user = save_mobile_device(user=user, mobile_device=mobile_device)
    return user
       

def get_user_mobile_device(user=None):
    try:
        apns_device = user.apns_device
        gcm_device = user.gcm_device
        if apns_device and gcm_device:
            #handle it need to uninstall in old one
            pass
        elif apns_device or gcm_device:
            if apns_device:
                return apns_device
            else:
                return gcm_device
        else:
            return None
    except Exception, e:
        print "error at mobile_utils get_user_mobile_device", str(e)
