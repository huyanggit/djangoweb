# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-13 01:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20170212_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='org',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg', verbose_name='\u6240\u5c5e\u673a\u6784'),
            preserve_default=False,
        ),
    ]
