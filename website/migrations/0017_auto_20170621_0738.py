# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-06-21 07:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0016_team_member_t_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team_leader',
            name='t_id',
        ),
        migrations.RemoveField(
            model_name='team_member',
            name='t_id',
        ),
        migrations.AddField(
            model_name='team_leader',
            name='u_id',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teams',
            name='t_members',
            field=models.ManyToManyField(to='website.team_member'),
        ),
        migrations.AlterField(
            model_name='proj_mngr',
            name='m_id',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='projects',
            name='admin',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='website.main_admin'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='m_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.student'),
        ),
        migrations.AlterField(
            model_name='projects',
            name='p_id',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]