# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-17 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecomments',
            name='comments',
            field=models.CharField(default='', max_length=200, verbose_name='\u8bc4\u8bba\u5185\u5bb9'),
        ),
    ]
