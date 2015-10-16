from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<device_key>[\w=-]+)/$', 'iot.monitor.views.details', name='Monitor details of particular device'),
    url(r'^device/$', 'iot.monitor.views.details', name='Monitor device from mobile '),
)
