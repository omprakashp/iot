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
from iot.users.models import log_visit, User, Devices, Applications, DeviceProperties, DevicesData
#to render the context instance to the template
#from django.template import *
#context_instance=RequestContext(request)

from iot.constants import CATEGORIES, get_categorywise_devices, get_features, clean_categories
from iot.generic.utils import details as generic_util_details
from iot.generic.utils import trigger as generic_trigger

@csrf_exempt
@cache_control(no_store=True, no_cache=True, must_revalidate=True,)
@login_required
def display_category_devices(request, category=None):
    #TODO: get the category user clicked!
    user = request.user
    result = generic_util_details(request, category, None)
    response = render_to_response('generic.html', {"title": category, "result": result , "categories": CATEGORIES})
    return response
 
@csrf_exempt
def trigger(request, encoded_key1=None):
    device_category= generic_trigger(request, encoded_key1)
    return HttpResponseRedirect('/iot/generic/%s/category_devices/' %(device_category))


