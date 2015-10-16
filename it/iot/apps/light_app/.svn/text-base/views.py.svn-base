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

DEVICE_CATEGORY = 'embedded'
APP_TYPE = 'light'

def details(request):
    #Find stats in between dates also
    #data = DevicesData.objects.filter(devices__user=request.user)
    #devices = data.values_list('devices', flat='true').distinct()
    result = embedded_utils.details(request, DEVICE_CATEGORY, APP_TYPE)
   
    return render_to_response('light_app.html', {'title': "embedded", 'result': result })

@csrf_exempt
def trigger(request, encoded_key1=None):
    result = embedded_utils.trigger(request, encoded_key1)
    return HttpResponseRedirect('/embedded/apps/light_app/details/') 
