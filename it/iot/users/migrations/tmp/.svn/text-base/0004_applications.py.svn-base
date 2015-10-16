# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_devices_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('app_name', models.CharField(max_length=100, null=True, verbose_name=b'Application name', blank=True)),
                ('app_category', models.CharField(max_length=100, null=True, verbose_name=b'Emb/ecomm/..', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('user', models.ManyToManyField(to='users.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
