# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 10:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0038_auto_20170623_1544'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='photo',
        ),
        migrations.AddField(
            model_name='student',
            name='model_pic',
            field=models.ImageField(default='/no-img.jpg', upload_to='MEDIA_ROOT'),
        ),
    ]
