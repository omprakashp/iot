# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_auto_20141124_1546'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device_Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'category name')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Device_Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name=b'device type')),
                ('properties', models.TextField(null=True, verbose_name=b'device type', blank=True)),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'created_date', editable=False)),
                ('modified_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Modified Date')),
                ('spare_1', models.CharField(max_length=100, null=True, verbose_name=b'Spare 1 field', blank=True)),
                ('spare_2', models.CharField(max_length=100, null=True, verbose_name=b'Spare 2 field', blank=True)),
                ('device_category', models.ForeignKey(blank=True, to='users.Device_Category', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='devices',
            name='device_category',
            field=models.ForeignKey(blank=True, to='users.Device_Category', null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='device_type',
            field=models.ForeignKey(blank=True, to='users.Device_Type', null=True),
        ),
        migrations.AlterField(
            model_name='devices',
            name='manufacturer',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name=b'Devi1ce manufacturer', choices=[(b'REGISTRATION', b'REGISTRATION'), (b'LOGIN', b'LOGIN'), (b'LOGOUT', b'LOGOUT'), (b'ON', b'ON'), (b'OFF', b'OFF')]),
        ),
    ]
