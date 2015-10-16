# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('push_notifications', '0001_initial'),
        ('users', '0007_devicesdata_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='apns_device',
            field=models.ForeignKey(blank=True, to='push_notifications.APNSDevice', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='devices',
            name='gcm_device',
            field=models.ForeignKey(blank=True, to='push_notifications.GCMDevice', null=True),
            preserve_default=True,
        ),
    ]
