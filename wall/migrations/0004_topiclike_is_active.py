# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-12 19:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0003_auto_20180912_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='topiclike',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
