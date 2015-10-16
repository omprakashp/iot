#!/var/www/www.embitel.com/virtualenvs/stage/bin/env python
import sys, os
sys.path.append('/var/www/www.embitel.com/it/iot/')
sys.path.append('/var/www/www.embitel.com/it/')
sys.path.append('/var/www/www.embitel.com/')

import settings
print 1
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iot.settings")
print "2>>>>", os.environ

import django
django.setup()

print "3 Django setup done"

from iot.users.models import Devices
print "Devices import is done"
from operator import add


from pyspark import SparkContext


if __name__ == "__main__":


    devices = Devices.objects.all().values()
    print devices

    sc = SparkContext(appName="IOT Test")


    data = list(Devices.objects.all().values_list('device_name', flat='true'))

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

    sc.stop()

