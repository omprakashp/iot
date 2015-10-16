# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20141111_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='applications',
            name='app_type',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Device type/app type', blank=True),
            preserve_default=True,
        ),
    ]
