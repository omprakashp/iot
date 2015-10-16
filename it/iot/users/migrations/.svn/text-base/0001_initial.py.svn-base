# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('push_notifications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_type', models.CharField(max_length=50, null=True, verbose_name=b'Device type/app type', blank=True)),
                ('app_name', models.CharField(max_length=100, null=True, verbose_name=b'Application name', blank=True)),
                ('app_category', models.CharField(max_length=100, null=True, verbose_name=b'Emb/ecomm/..', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device_Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'category name')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'device type')),
                ('properties', models.TextField(null=True, verbose_name=b'device type', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('device_category', models.ForeignKey(blank=True, to='users.Device_Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DeviceProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_state', models.CharField(default=b'OFF', max_length=20, verbose_name=b'ON/OFF')),
                ('dim', models.CharField(default=b'70', max_length=20, null=True, verbose_name=b'1-100 range', blank=True)),
                ('color', models.CharField(max_length=20, null=True, verbose_name=b'color code', blank=True)),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Devices',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True, verbose_name=b'Active/incative')),
                ('device_id', models.CharField(unique=True, max_length=50, verbose_name=b'Device Name')),
                ('device_name', models.CharField(max_length=50, null=True, verbose_name=b'Device Name', blank=True)),
                ('device_ip', models.CharField(max_length=50, null=True, verbose_name=b'Device IP', blank=True)),
                ('manufacturer', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Devi1ce manufacturer', choices=[(b'REGISTRATION', b'REGISTRATION'), (b'LOGIN', b'LOGIN'), (b'LOGOUT', b'LOGOUT'), (b'ON', b'ON'), (b'OFF', b'OFF')])),
                ('warranty', models.DateTimeField(null=True, verbose_name=b'Warranty ends on', blank=True)),
                ('current_state', models.CharField(default=b'OFF', max_length=20, verbose_name=b'ON/OFF')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('device_features', models.TextField(null=True, verbose_name=b'Features opted in str(list) format', blank=True)),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('device_type', models.ForeignKey(blank=True, to='users.Device_Type', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DevicesData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('data', models.TextField(null=True, blank=True)),
                ('message_id', models.CharField(max_length=100, null=True, blank=True)),
                ('sent', models.BooleanField(default=False, verbose_name=b'To check message sent or not')),
                ('delivered', models.BooleanField(default=False, verbose_name=b'To check message delivered')),
                ('received', models.BooleanField(default=False, verbose_name=b'To check message delivered')),
                ('action', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Action Performed', choices=[(b'REGISTRATION', b'REGISTRATION'), (b'LOGIN', b'LOGIN'), (b'LOGOUT', b'LOGOUT'), (b'ON', b'ON'), (b'OFF', b'OFF')])),
                ('email', models.EmailField(max_length=100, null=True, blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('devices', models.ForeignKey(blank=True, to='users.Devices', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('selected_channels', models.CharField(max_length=50, null=True, verbose_name=b'Ecomm/Embedded/Mob/Auto', blank=True)),
                ('selected_services', models.CharField(max_length=50, null=True, verbose_name=b'Services', blank=True)),
                ('dob', models.DateField(max_length=300, null=True, verbose_name=b'Date of Birth', blank=True)),
                ('visitor_ip', models.CharField(max_length=30, null=True, verbose_name=b'IP Address', blank=True)),
                ('is_paid', models.BooleanField(default=False, verbose_name=b'paid for all services opted or not')),
                ('mobile_number', models.CharField(max_length=10, null=True, verbose_name=b'Mobile Number', blank=True)),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('apns_device', models.ForeignKey(related_name=b'apns_mobile_device', blank=True, to='push_notifications.APNSDevice', null=True)),
                ('gcm_device', models.ForeignKey(related_name=b'gcm_mobile_device', blank=True, to='push_notifications.GCMDevice', null=True)),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
        ),
        migrations.CreateModel(
            name='Visitors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(max_length=40, null=True, verbose_name=b'session key', blank=True)),
                ('url_visited', models.CharField(max_length=300, null=True, verbose_name=b'Last URL Visited', blank=True)),
                ('visit_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Time of Action')),
                ('visitor_ip', models.CharField(max_length=30, null=True, verbose_name=b'IP Address', blank=True)),
                ('email', models.CharField(max_length=75, null=True, verbose_name=b'e-mail address of logged in user', blank=True)),
                ('referral', models.CharField(max_length=300, null=True, verbose_name=b'Referred By', blank=True)),
                ('source', models.CharField(max_length=50, null=True, verbose_name=b'Source ', blank=True)),
                ('action', models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Action Performed', choices=[(b'REGISTRATION', b'REGISTRATION'), (b'LOGIN', b'LOGIN'), (b'LOGOUT', b'LOGOUT'), (b'ON', b'ON'), (b'OFF', b'OFF')])),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='devices',
            name='user',
            field=models.ManyToManyField(to='users.User'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deviceproperties',
            name='device',
            field=models.OneToOneField(null=True, blank=True, to='users.Devices'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applications',
            name='devices',
            field=models.ManyToManyField(to='users.Devices'),
            preserve_default=True,
        ),
    ]
