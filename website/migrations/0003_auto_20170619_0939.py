# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-19 09:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_team_member_name'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='admin',
            new_name='main_admin',
        ),
    ]
