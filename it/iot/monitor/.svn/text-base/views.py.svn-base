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

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import AnonymousUser

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.cache import cache_control

from django.db import transaction
#to render the context instance to the template
#from django.template import *
#context_instance=RequestContext(request)

from iot.constants import CATEGORIES
from iot.monitor.utils import details as generic_util_details

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
def details(request, device_key=None):
    source = ''
    try:
        data = eval(str(request.body))
        source = 'mobile'
        device_key = data['id']
    except:
        data = request.POST.copy()

    if source == 'mobile':
        result = generic_util_details(request, device_key, source)
        return HttpResponse(json.dumps(result), content_type='application/json')

    data_usage_graph_values, time_interval_graph_values = generic_util_details(request, device_key, source)
    response = render_to_response('monitor_light.html', { "result": data_usage_graph_values,  "time_intervals": time_interval_graph_values, "categories": CATEGORIES, "device_id":device_key})
    return response
