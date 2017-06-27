# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-20 10:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0012_auto_20170620_1037'),
    ]

    operations = [
        migrations.CreateModel(
            name='work_log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('w_id', models.CharField(blank=True, max_length=250)),
                ('desc', models.CharField(max_length=1000)),
                ('s_id', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.student')),
                ('t_id', models.ForeignKey(blank=True, default='0', on_delete=django.db.models.deletion.CASCADE, to='website.teams')),
            ],
        ),
    ]