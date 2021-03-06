# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-01 11:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('action', '0001_initial'),
        ('trigger', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_checked', models.DateTimeField(auto_now=True)),
                ('trigger_params', models.TextField(default='{}')),
                ('action_params', models.TextField(default='{}')),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='action.Action')),
                ('trigger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trigger.Trigger')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
