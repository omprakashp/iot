from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'^details/$', 'iot.embedded.apps.light_app.views.details', name='details'),
    url(r'^(?P<encoded_key1>[\w=-]+)/trigger/', 'iot.embedded.apps.light_app.views.trigger', name='On Off trigger'),
)
