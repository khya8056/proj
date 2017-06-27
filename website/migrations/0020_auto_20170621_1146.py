# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-21 11:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0019_auto_20170621_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team_member',
            name='mem_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.student'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='p_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.projects'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='t_id',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='teams',
            name='t_leader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.student'),
        ),
        migrations.AlterField(
            model_name='teams',
            name='t_members',
            field=models.ManyToManyField(blank=True, to='website.team_member'),
        ),
    ]
