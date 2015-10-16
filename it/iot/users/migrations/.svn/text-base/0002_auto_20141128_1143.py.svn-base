# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceproperties',
            name='swing_state',
            field=models.CharField(default=b'OFF', max_length=20, verbose_name=b'ON/OFF'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='deviceproperties',
            name='temperature',
            field=models.CharField(default=b'20', max_length=20, null=True, verbose_name=b'1-100 range', blank=True),
            preserve_default=True,
        ),
    ]
