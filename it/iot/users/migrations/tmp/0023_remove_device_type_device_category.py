# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_auto_20141127_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device_type',
            name='device_category',
        ),
    ]
