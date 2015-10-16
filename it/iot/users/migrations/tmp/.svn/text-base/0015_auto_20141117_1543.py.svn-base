# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_devices_device_features'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceProperties',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current_state', models.CharField(default=b'OFF', max_length=20, verbose_name=b'ON/OFF')),
                ('dim', models.IntegerField(null=True, verbose_name=b'1-100 range', blank=True)),
                ('color', models.CharField(max_length=20, null=True, verbose_name=b'color code', blank=True)),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='devices',
            name='device_properties',
            field=models.OneToOneField(null=True, blank=True, to='users.DeviceProperties'),
            preserve_default=True,
        ),
    ]
