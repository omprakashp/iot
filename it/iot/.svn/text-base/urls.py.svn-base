from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'iot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #TODO: admin urls required??
    #url(r'^admin/', include(admin.site.urls)),

    #url(r'^ecommerce/', include('iot.ecommerce.urls')),
    #url(r'^embedded/', include('iot.embedded.urls')),
    #url(r'^automation/', include('iot.automation.urls')),
    url(r'^iot/generic/', include('iot.generic.urls')),
    url(r'^iot/monitor/', include('iot.monitor.urls')),



    #TODO: use single function and maintain comnstants file to render data and also based up on the url just serve data to frontend
    url(r'^iot/dashboard/$', 'iot.views.dashboard', name='dashboard'),
    url(r'^iot/dashboard/proc/$', 'iot.views.dashboard_proc', name='dashboard edit'),
    url(r'^iot/device_management/$', 'iot.views.device_management', name='Device Managament'),
    #url(r'^ecommerce/$', 'iot.views.ecommerce', name='Ecommerce Home Page'),
    #url(r'^embedded/$', 'iot.views.embedded', name='Embedded Home Page'),
    #url(r'^automation/$', 'iot.views.automation', name='Autoamtion Home Page'),

    url(r'^devices/details/autocar/', 'iot.views.autocar', name='Remote car'),
    url(r'^devices/configure_ajax/auto_car/', 'iot.views.autocar_ajax', name='change of angle and speed'),
    url(r'^devices/details/(?P<device_key>[\w=-]+)/', 'iot.views.device_details_display', name='Device details'),
    url(r'^devices/add_device/$', 'iot.views.add_device', name='Button to add new device'),
    url(r'^devices/add_device/proc/$', 'iot.views.add_device_proc', name='Adding new device'),
    url(r'^devices/delete/(?P<device_key>[\w=-]+)/$', 'iot.views.delete_device', name='to add user for access'),
    url(r'^devices/configure/(?P<device_key>[\w=-]+)/proc/', 'iot.views.configure_device_proc', name='configure features save and redirect'),
    url(r'^devices/configure/(?P<device_key>[\w=-]+)/', 'iot.views.configure_device', name='configure features'),
    url(r'^iot/configure_ajax/$', 'iot.views.configure_device_ajax', name='dashboard'),
    url(r'^iot/devices/(?P<device_key>[\w=-]+)/add_user/$', 'iot.views.configure_device_add_user', name='to add user for access'),
    url(r'^iot/devices/(?P<device_key>[\w=-]+)/(?P<user_key>[\w=-]+)/delete_user/$', 'iot.views.configure_device_delete_user', name='del user'),
    url(r'^iot/devices/(?P<device_key>[\w=-]+)/map_device/$', 'iot.views.configure_device_map_device', name='Event based actions'),
    url(r'^devices/my_events/$', 'iot.views.my_events', name='Display and configure events'),
    url(r'^devices/my_events/proc/$', 'iot.views.my_events_proc', name='Display and configure events'),
    url(r'^devices/handle_events/$', 'iot.views.handle_events', name='Handle events'),
    url(r'^devices/handle_events/(?P<selected_event>[\w=-]+)/$', 'iot.views.handle_events', name='Handle events from web'),
    url(r'^devices/my_events/(?P<event_id>[\w=-]+)/delete/$', 'iot.views.delete_event', name='to delete event'),
    url(r'^devices/my_patterns/$', 'iot.views.my_patterns', name='Display and configure rules'),
    ##FOR MOBILE APPLICATIONS TO GET JSON RESPONSE
    url(r'^mobile/login/$', 'iot.views.login_proc', name='login_proc'),
    url(r'^categories/$', 'iot.views.get_categories', name='To get the available categories'),
    url(r'^mobile/devices/add_device/$', 'iot.views.add_device_proc', name='Adding new device from mobile'),
    url(r'^mobile/devices/get_devices/$', 'iot.views.get_registered_devices', name='Get all registered devices under individual category'),
    url(r'^mobile/devices/get_device_details/$', 'iot.views.get_device_details', name='Get device details'),
    url(r'^mobile/devices/configure/', 'iot.views.configure_device_proc', name='configure features saved from mobile'),
    url(r'^mobile/devices/geofence/', 'iot.views.geo_fencing_action', name='ON and OFF as per geofence'),
    url(r'^mobile/devices/my_events/$', 'iot.views.my_events', name='mobile- display events'),
    url(r'^mobile/devices/handle_events/$', 'iot.views.handle_events', name='Handle events'),
    url(r'^mobile/devices/my_events/add/$', 'iot.views.my_events_proc', name='Display and configure events'),
    url(r'^mobile/devices/my_events/get_device_types/$', 'iot.views.get_devicetypes_and_devices', name='Sends all devices under each device_type'),
    url(r'^mobile/devices/media_event/$', 'iot.views.media_event', name='Display and configure events'),
    url(r'^mobile/devices/autocar_mode/$', 'iot.views.AutoCar_mode', name='To change mode to manual control or Auto control'),

    #For any other sensors or devices
    url(r'^sensor/devices/configure/', 'iot.views.configure_device_proc', name='configure features saved from any other sensors'),
    url(r'^sensor/devices/get_device_details/$', 'iot.views.get_device_details', name='Get device details'),
    url(r'^sensor/devices/update_ip/$', 'iot.views.update_hardware_IP', name='Update IP for devices'),


    url(r'^testing/$', 'iot.views.testing', name='testing'),


    url(r'^work_in_progress/$', 'iot.views.construction', name='work in progress'),
    url(r'^login/$', 'iot.views.reg_login', name='login'),
    url(r'^login?next=/embitel/dashboard/configure_notifications/$', 'iot.views.reg_login', name='login'),
    url(r'^register/$', 'iot.views.register', name='registration'),
    url(r'^unregister/(?P<encoded_key1>[\w=-]+)/', 'iot.views.unregister', name='unregister'),
    url(r'^login/proc/$', 'iot.views.login_proc', name='login_proc'),
    url(r'^logout/$', 'iot.views.logout_view', name='logout'),
    url(r'^.*', 'iot.views.redirect_default_page', name='Default page for unknown urls'),    
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
