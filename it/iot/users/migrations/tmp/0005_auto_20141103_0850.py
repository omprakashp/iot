# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_applications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='applications',
            name='user',
        ),
        migrations.AddField(
            model_name='applications',
            name='devices',
            field=models.ManyToManyField(to='users.Devices'),
            preserve_default=True,
        ),
    ]
