#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python
import sys, os
sys.path.append(os.path.abspath('..'))
sys.path.append('/var/www/www.embitel.com/it/iot')
sys.path.append('/var/www/www.embitel.com/it/')
import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")

import django
django.setup()


from iot.users.models import Devices

devices = list(Devices.objects.all().values_list('device_name', flat='true'))

print "length of devices: %s" %len(devices)

