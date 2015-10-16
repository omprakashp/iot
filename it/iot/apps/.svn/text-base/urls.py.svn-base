from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),

    #url(r'^admin/', include(admin.site.urls)),
    #url(r'^test/$', 'iot.mobility.views.test', name='test'),
    url(r'^temperature_sensor/', include('iot.embedded.apps.temperature_sensor.urls')),
    url(r'^light_app/', include('iot.embedded.apps.light_app.urls')),
    url(r'^switch_sensor/', include('iot.embedded.apps.switch_sensor.urls')),
)
