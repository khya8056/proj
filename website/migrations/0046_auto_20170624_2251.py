# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-24 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0045_uploadmodel_p_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadmodel',
            name='p_id',
            field=models.ForeignKey(blank='True', on_delete=django.db.models.deletion.CASCADE, to='website.projects'),
        ),
    ]