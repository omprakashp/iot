from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^details/$', 'iot.embedded.apps.temperature_sensor.views.details', name='details'),
    url(r'^(?P<encoded_key1>[\w=-]+)/trigger/', 'iot.embedded.apps.temperature_sensor.views.trigger', name='On Off trigger'),
    url(r'^save_data/$', 'iot.embedded.apps.temperature_sensor.views.save_data', name='save data from sensors'),
)
