# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-23 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0035_main_admin_photo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='main_admin',
            name='photo',
        ),
        migrations.AddField(
            model_name='main_admin',
            name='model_pic',
            field=models.ImageField(default='media/no-img.jpg', upload_to='media/'),
        ),
    ]
