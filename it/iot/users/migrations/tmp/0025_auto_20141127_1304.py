# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0024_auto_20141127_1302'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devices',
            name='device_category',
        ),
        migrations.DeleteModel(
            name='Device_Category',
        ),
    ]
