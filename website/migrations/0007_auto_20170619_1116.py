# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-19 11:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_auto_20170619_1000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='main_admin',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='main_admin',
            name='email',
        ),
        migrations.RemoveField(
            model_name='main_admin',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='main_admin',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='proj_mngr',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='proj_mngr',
            name='email',
        ),
        migrations.RemoveField(
            model_name='proj_mngr',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='proj_mngr',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='email',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='last_name',
        ),
    ]