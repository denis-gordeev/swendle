# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-23 13:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0024_auto_20170821_2152'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='bias',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
