# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-12 09:56
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_created=True, default=datetime.datetime.now)),
                ('body', models.TextField(max_length=200)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wall.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='TopicLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.DateTimeField(auto_created=True, default=datetime.datetime.now)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wall.Topic')),
            ],
        ),
    ]
