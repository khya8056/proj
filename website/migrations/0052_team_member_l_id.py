# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-27 06:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0051_auto_20170626_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='team_member',
            name='l_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='website.team_leader'),
            preserve_default=False,
        ),
    ]
