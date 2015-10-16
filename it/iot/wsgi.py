"""
WSGI config for iot project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
import sys
import site

sys.stdout = sys.stderr

# Project root
root = '/var/www/www.embitel.com/it/'
sys.path.insert(0, root)

# Packages from virtualenv
activate_this = '/var/www/www.embitel.com/virtualenvs/stage/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

# Set environmental variable for Django and fire WSGI handler 
os.environ['DJANGO_SETTINGS_MODULE'] = 'iot.settings'
#os.environ['DJANGO_CONF'] = 'conf.stage'
os.environ["CELERY_LOADER"] = "django"

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

