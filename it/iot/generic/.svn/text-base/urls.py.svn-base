from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<category>[\w=-]+)/category_devices/$', 'iot.generic.views.display_category_devices', name='test'),
    url(r'^device_state/(?P<encoded_key1>[\w=-]+)/trigger/', 'iot.generic.views.trigger', name='trigger on / off'),
)
