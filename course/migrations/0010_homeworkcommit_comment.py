# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-02-23 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0009_auto_20180114_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='homeworkcommit',
            name='comment',
            field=models.TextField(blank=True, null=True),
        ),
    ]
