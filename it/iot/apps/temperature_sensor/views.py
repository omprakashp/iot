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

from iot.embedded.apps import utils as embedded_utils
from iot.users.models import Applications

DEVICE_CATEGORY = 'embedded'
APP_TYPE = 'temperature'

def details(request):
    result = embedded_utils.details(request, DEVICE_CATEGORY, APP_TYPE)

    return render_to_response('temperature_sensor.html', {'title': "embedded", 'result': result })

@csrf_exempt
def trigger(request, encoded_key1=None):
    result = embedded_utils.trigger(request, encoded_key1)
    return HttpResponseRedirect('/embedded/apps/temperature_sensor/details/')

@csrf_exempt
def save_data(request):
    # This is just to store data of temperature temporarily Hardcoded
    data = request.POST
    device = Applications.objects.get(app_name=APP_NAME).devices.all()[0]
    device_data = DevicesData.objects.create(data=data['temperature'], spare_1=data['id'], devices=device, action="ON")
    device.save()
    device_data = DevicesData.objects.create(devices=device, spare_1=data['id'], action="OFF")
    device.save()
    result = {"success": True}
    return HttpResponse(json.dumps(result), content_type='application/json')
