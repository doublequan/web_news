# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-09 08:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('interviews', '0007_auto_20160709_0801'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
