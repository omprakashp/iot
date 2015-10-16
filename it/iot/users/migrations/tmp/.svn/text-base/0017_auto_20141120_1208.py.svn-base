# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0001_initial'),
        ('users', '0016_auto_20141120_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='apns_device',
            field=models.ForeignKey(related_name=b'apns_mobile_device', blank=True, to='push_notifications.APNSDevice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='gcm_device',
            field=models.ForeignKey(related_name=b'gcm_mobile_device', blank=True, to='push_notifications.GCMDevice', null=True),
            preserve_default=True,
        ),
    ]
