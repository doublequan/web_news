# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0009_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='create_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]