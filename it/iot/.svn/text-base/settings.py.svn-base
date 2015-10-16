"""
Django settings for iot project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
location = lambda x: os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', x)
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0*0+zkr+gzi1$e#%idr$&+p+9rl4k0+w+06=6%*9_b25q9)w6&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALL_DIRECTORY ='/var/www/www.embitel.com/' 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/


import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATICFILES_DIRS = (
    #os.path.join(PROJECT_ROOT, 'static'),
    os.path.join(PROJECT_ROOT, 'static/images'),
    os.path.join(PROJECT_ROOT, 'static/css'),
    os.path.join(PROJECT_ROOT, 'static/js'),
)


STATIC_URL = '/static/'
#STATIC_ROOT= '/var/www/www.embitel.com/static/'
STATIC_ROOT = location('static')

MEDIA_URL = '/media/'
#STATIC_ROOT= '/var/www/www.embitel.com/static/'
MEDIA_ROOT = location('media')

#STATICFILES_DIRS = (
#    os.path.join(BASE_DIR, "static"),
#    '/var/www/static/',
#)

# Application definition

#TEMPLATE_LOADERS = (
#    #'django.template.loaders.filesystem.load_template_source',
#    'django.template.loaders.app_directories.load_template_source',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
#    )


TEMPLATE_DIRS = (
    INSTALL_DIRECTORY + "it/iot/templates/",
    INSTALL_DIRECTORY + "it/iot/templates/includes",
    INSTALL_DIRECTORY + "it/iot/core/templates",    
    INSTALL_DIRECTORY + "it/iot/generic/templates",    
    INSTALL_DIRECTORY + "it/iot/monitor/templates",    
    INSTALL_DIRECTORY + "it/iot/apps/templates",    
    #Auth
    #INSTALL_DIRECTORY + "django/contrib/auth/templates",
   )

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'push_notifications',
    'iot',
    'iot.core',
    'iot.users',
    'iot.generic',
    'iot.apps',
    #'iot.mobility.apps.testapp1',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'iot.urls'

WSGI_APPLICATION = 'iot.wsgi.application'

#MObile related stuff
GCM_POST_URL = 'https://android.googleapis.com/gcm/send'
PUSH_NOTIFICATIONS_SETTINGS = {
        "GCM_API_KEY": "AIzaSyBxoHN9oAHviBkXyavhH3mJvq4PZS3WTwo",
        "APNS_CERTIFICATE": "/var/www/www.embitel.com/it/apns-development.pem",
}


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

#TODO: Check how to use multiple databases and how can they connect to each other
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'iot', # Or path to database file if using sqlite3.
        'USER': 'iot', # Not used with sqlite3.
        'PASSWORD': 'iot',#'84adf87feae4a6f0c63f0a3df7d6c456', # Not used with sqlite3.
        'HOST': '127.0.0.1', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    },
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Calcutta'#'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False



