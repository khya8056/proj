# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-22 06:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0024_work_log_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='work_log',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 6, 22, 6, 29, 34, 185943)),
        ),
    ]
