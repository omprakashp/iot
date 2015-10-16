# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_auto_20141121_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='device_properties',
        ),
        migrations.AddField(
            model_name='deviceproperties',
            name='device',
            field=models.OneToOneField(null=True, blank=True, to='users.Devices'),
            preserve_default=True,
        ),
    ]
