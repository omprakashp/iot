# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20141121_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceproperties',
            name='dim',
            field=models.CharField(default=b'70', max_length=20, null=True, verbose_name=b'1-100 range', blank=True),
        ),
    ]
