# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-23 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0044_auto_20170623_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='uploadmodel',
            name='p_id',
            field=models.ForeignKey(blank=b'True', default=0, on_delete=django.db.models.deletion.CASCADE, to='website.projects'),
            preserve_default=False,
        ),
    ]
