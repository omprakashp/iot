from django.db import models
from django.contrib.auth.models import User as user

from django.db.models.signals import post_save
import datetime

from iot.constants import POSSIBLE_ACTIONS 

from push_notifications.models import GCMDevice, APNSDevice
import iot.moonutils as it_utils
from collections import OrderedDict
from django.dispatch import receiver

class User(user):

    # Check whether we can do seperate table and relation ship withn Channels and Services with FK/many-to-many  relation
    #user = models.OneToOneField(User)
    selected_channels = models.CharField('Ecomm/Embedded/Mob/Auto', max_length=50, blank = True, null=True)
    selected_services = models.CharField('Services', max_length=50, blank = True, null=True)
    dob  = models.DateField("Date of Birth", blank = True, null=True, max_length=300)
    visitor_ip = models.CharField("IP Address", blank = True, null=True, max_length=30)
    is_paid = models.BooleanField("paid for all services opted or not", default= False)
    mobile_number = models.CharField(('Mobile Number'),blank = True, null=True, max_length=10)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)
    created_date = models.DateTimeField("created_date", editable=False, default = datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    apns_device = models.ForeignKey(APNSDevice, null=True, blank=True, related_name="apns_mobile_device")
    gcm_device = models.ForeignKey(GCMDevice, null=True, blank=True, related_name="gcm_mobile_device")


    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(User, self).save(*args, **kwargs)


class Device_Category(models.Model):
    name = models.CharField("category name", max_length=50, unique=True)#light
    created_date = models.DateTimeField("created_date", editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(Device_Category, self).save(*args, **kwargs)


class Device_Type(models.Model):
    name = models.CharField("device type", max_length=50, unique=True)#light
    device_category = models.ForeignKey(Device_Category, null=True, blank=True)
    properties = models.TextField("device type", blank=True, null=True )
    created_date = models.DateTimeField("created_date", editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(Device_Type, self).save(*args, **kwargs)


class Devices(models.Model):
    #TODO: modified date not changing
    #TODO: decide unique constraint /  unique to gether for devices
    #TODO: Device last used on and how much time used should be updated using django signals when DevicesData is updated/created
    user = models.ManyToManyField(User) #N number of devices connected to N number of users
    #device_properties = models.OneToOneField(DeviceProperties, null=True, blank=True)#create a Property instance along with the device with out blank
    active = models.BooleanField("Active/incative", default=True)
    device_id = models.CharField('Device Name', max_length=50)#, unique=True)  #Yeelight device ids are same for different gateways
    device_name = models.CharField('Device Name', max_length=50, blank = True, null=True)
    device_ip = models.CharField('Device IP', max_length=50, blank = True, null=True)
    #device_category = models.ForeignKey(Device_Category, null=True, blank=True)
    device_type = models.ForeignKey(Device_Type, null=True, blank=True)
    manufacturer = models.CharField('Devi1ce manufacturer', choices = POSSIBLE_ACTIONS, max_length = 30, blank=True, null=True)
    warranty = models.DateTimeField("Warranty ends on", null=True, blank=True)
    current_state = models.CharField("ON/OFF", max_length=20, default="OFF")
    created_date = models.DateTimeField("created_date", editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    device_features = models.TextField('Features opted in str(list) format', blank=True, null=True)
    owner = models.EmailField('owner email address', null=True, blank=True)
    mapped_devices = models.TextField("device type", default='[]')
    gateway_ip = models.CharField('GATEWAY IP(socket communication)', max_length=50, blank = True, null=True)
    gateway_port = models.IntegerField('GATEWAY PORT(socket communication)', max_length=50, blank = True, null=True)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

    #unique_together = (("device_id", "device_ip"),)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(Devices, self).save(*args, **kwargs)


OPEN_CLOSE_STATES = (("CLOSE", "CLOSE"), ("OPEN", "OPEN"))

class DeviceProperties(models.Model):
    device = models.OneToOneField(Devices, null=True, blank=True)#create a Property instance along with the device with out blank

    #Light
    current_state = models.CharField("ON/OFF", max_length=20, default="OFF")#light
    dim = models.IntegerField("1-100 range", blank=True, null=True, max_length=20, default="70")
    rgb_r = models.IntegerField("color code", max_length=10, default=255)
    rgb_g = models.IntegerField("color code", max_length=10, default=255)
    rgb_b = models.IntegerField("color code", max_length=10, default=255)
    rgb = models.CharField("color code", max_length=10, blank=True, null=True)

    #AC
    temperature = models.CharField("1-100 range", blank=True, null=True, max_length=20, default="0")
    swing_state = models.CharField("ON/OFF", max_length=20, default="OFF")
   
    #Car Head unit
    speed = models.CharField("speed kph", blank=True, null=True, max_length=20, default="0")
    rpm = models.CharField("RPM", blank=True, null=True, max_length=20, default="0")
    car_ac = models.CharField("ON/OFF", max_length=20, default="OFF")#light
    mode = models.CharField("auto or mannual car driving", max_length=20, null=True, blank=True)
    drive_mode = models.CharField("follow/avoid/lane", max_length=20, null=True, blank=True)
    car_light = models.CharField("ON/OFF", max_length=20, default="OFF")#light
    car_door = models.CharField("ON/OFF", max_length=20, default="OFF")#light

    #Door state
    door_state = models.CharField("OPEN / CLOSE", max_length=20, choices=OPEN_CLOSE_STATES, default="CLOSE")

    #BlindSlats
    blinds_state = models.CharField("OPEN / CLOSE", max_length=20, choices=OPEN_CLOSE_STATES, default="CLOSE")
    slats_state = models.CharField("OPEN / CLOSE", max_length=20, choices=OPEN_CLOSE_STATES, default="CLOSE")

    #BEacons
    zone = models.IntegerField("0-out of range, 1-near to beacon, 2-moving far from beacon", max_length=10, blank=True, null=True)
    zone_flag = models.BooleanField("Zone flag", default=False) #if any data sent from cloud to device

    spare_1 = models.CharField(('Spare 1 field'),blank=True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank=True, null=True, max_length=100)


    def set_val(self, dict):
        it_utils.it_set_val(self, dict)
        if 'rgb_r' and 'rgb_b'  and 'rgb_g' in eval(self.device.device_type.properties).values():
            try:
                self.rgb = '#' + "".join(map(chr, (int(self.rgb_r), int(self.rgb_g), int(self.rgb_b)))).encode('hex')
            except:
                pass

        self.save()
        return

    def get_my_properties(self):
        if not self.device:
            return None
        #device_properties = self.device.device_type.properties
        #TODO: do get_val to get the required dict
       

@receiver(post_save, sender=DeviceProperties)
def abc(sender, **kwargs):
    obj = kwargs['instance']
    device = obj.device
    device.current_state = obj.current_state
    device.save()
    #if kwargs.get('created', False):
    #    UserProfile.objects.get_or_create(user=kwargs.get('instance'))
    return


class UserEvents(models.Model):
    user = models.ForeignKey(User) #N number of devices connected to N number of users
    name = models.CharField('Event Name', max_length=50, blank = True, null=True)
    properties = models.TextField('Event properties in dict', blank = True, null=True)
    event_trigger_time = models.CharField("trigger this event at", max_length=10, blank=True, null=True)
    active = models.BooleanField("devices will be activated if active flag is True", default=True) 
    repeat_on = models.CharField("1-7days trigger this event repeatedly on these days", max_length=20, blank=True, null=True)
    created_date = models.DateTimeField("created_date", editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(UserEvents, self).save(*args, **kwargs)


class Applications(models.Model):
    devices = models.ManyToManyField(Devices) #N number of devices connected to N number of users
    app_type = models.CharField('Device type/app type', max_length=50, blank = True, null=True) 
    app_name = models.CharField(('Application name'),blank = True, null=True, max_length=100)
    app_category = models.CharField(('Emb/ecomm/..'),blank = True, null=True, max_length=100)
    created_date = models.DateTimeField("created_date", editable=False, default=datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)
    #unique_together = (("device_id", "device_ip"),)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(Applications, self).save(*args, **kwargs)

class DevicesData(models.Model):
    data = models.TextField(null=True, blank=True)
    message_id = models.CharField(max_length=100, null=True, blank=True)
    devices = models.ForeignKey(Devices, null=True, blank=True)
    sent = models.BooleanField("To check message sent or not", default=False) #if any data sent from cloud to device
    delivered = models.BooleanField("To check message delivered", default=False)# if sent data is delivered or not (ACK)
    received = models.BooleanField("To check message delivered", default=False) #For data just recieved from devices use this flag
    action = models.CharField('Action Performed', choices = POSSIBLE_ACTIONS, max_length = 30, blank=True, null=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField("created_date", editable=False, default = datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(DevicesData, self).save(*args, **kwargs)


class Visitors(models.Model):

    def now():
        return datetime.datetime.now()

    #Session details
    session_key = models.CharField('session key', max_length=40, blank = True, null=True)
    url_visited  = models.CharField("Last URL Visited", blank = True, null=True, max_length=300)
    visit_time = models.DateTimeField('Time of Action', default=datetime.datetime.now)
    visitor_ip = models.CharField("IP Address", blank = True, null=True, max_length=30)
    email = models.CharField(('e-mail address of logged in user'),blank = True, null=True, max_length=75)
    referral  = models.CharField("Referred By", blank = True, null=True, max_length=300)
    source  = models.CharField("Source ", blank = True, null=True, max_length=50)
    action = models.CharField('Action Performed', choices = POSSIBLE_ACTIONS, max_length = 30, blank=True, null=True)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)

def log_visit(request=None, action = 'NotProvided', email = None, source = 'kewl'):
    visitor_log = Visitors()
    try:
        if request != None:
            visitor_log.url_visited = request.META['PATH_INFO'][:299]
            if 'HTTP_X_FORWARDED_FOR' in request.META:
                try:
                    visitor_log.visitor_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
                except Exception,e:
                    print "Error while fetching the IP", str(e)
                    pass
            else:
                visitor_log.visitor_ip = request.META['REMOTE_ADDR']

            if action in ['NotProvided',]:
                action = 'Surfing'
            try:
                visitor_log.email = request.user.email
            except:
                pass
            try:
                visitor_log.referral = request.META['HTTP_REFERER'][:299]
            except:
                visitor_log.referral = 'direct'
        visitor_log.action = action
        if email:
            visitor_log.email = email
        if source:
            visitor_log.source = source
        visitor_log.save()
    except Exception, e:
        pass


class SocketCommands(models.Model):
    command = models.TextField("json to be sent to client via active socket connection")
    send_to = models.CharField('send to email id, usefull for mqtt subscriptions', blank = True, null=True, max_length=100)
    publish_url = models.TextField('mqtt subscriptions', blank = True, null=True)

#machine recognized patterns
class DevicesPatterns(models.Model):
    on_at = models.TextField("devices regularly on at", default='')
    off_at = models.TextField("devices regularly off at", default='')
    data = models.TextField("any data", default='[]')
    devices = models.ForeignKey(Devices, null=True, blank=True)
    most_utilized_device = models.BooleanField("Most utilized device or not", default= False)
    created_date = models.DateTimeField("created_date", editable=False, default = datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)
    

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(DevicesPatterns, self).save(*args, **kwargs)

#user accepted patterns
class DevicesRules(models.Model):
    rule_name = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=50)
    rules = models.TextField("device rules",  null=True, blank=True)
    data = models.TextField("any data",  null=True, blank=True)
    created_date = models.DateTimeField("created_date", editable=False, default = datetime.datetime.now)
    modified_date = models.DateTimeField("Modified Date", default = datetime.datetime.now)
    spare_1 = models.CharField(('Spare 1 field'),blank = True, null=True, max_length=100)
    spare_2 = models.CharField(('Spare 2 field'),blank = True, null=True, max_length=100)
    

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created_date = datetime.datetime.today()
        self.modified_date = datetime.datetime.today()
        return super(DevicesRules, self).save(*args, **kwargs)

class AutoCar(models.Model):
    command = models.TextField("Command from mobile")
    speed = models.IntegerField("1-100 range", default=10)
    angle = models.IntegerField("1-180 range", blank = True, null=True)
    send_to = models.CharField('send to gateway', blank = True, null=True, max_length=100)
    sent = models.BooleanField("sent to gateway?", default= False)
    publish_url = models.TextField('mqtt subscriptions', blank = True, null=True)
    mode = models.CharField('auto mode or manual mode', max_length=20, blank = True, null=True)
    drive_mode = models.CharField('follow or avoid  mode', max_length=20, blank = True, null=True)
    distance = models.IntegerField('distance from obstacles', max_length=20, blank = True, null=True)

