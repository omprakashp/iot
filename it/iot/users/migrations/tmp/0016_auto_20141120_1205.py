# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_auto_20141117_1543'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='apns_device',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='gcm_device',
        ),
    ]
