# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-12 00:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20161231_0638'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='text',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]