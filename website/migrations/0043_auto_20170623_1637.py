# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0042_auto_20170623_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_admin',
            name='model_pic',
            field=models.ImageField(default='/no-img.jpg', upload_to='MEDIA_ROOT'),
        ),
    ]
