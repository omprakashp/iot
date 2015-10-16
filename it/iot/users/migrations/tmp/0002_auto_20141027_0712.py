# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Device manufacturer', choices=[(b'REGISTRATION', b'REGISTRATION'), (b'LOGIN', b'LOGIN'), (b'LOGOUT', b'LOGOUT'), (b'ON', b'ON'), (b'OFF', b'OFF')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='devices',
            name='warranty',
            field=models.DateTimeField(null=True, verbose_name=b'Warranty ends on', blank=True),
            preserve_default=True,
        ),
    ]
