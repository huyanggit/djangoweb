# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-02-16 15:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_need',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='\u8bfe\u7a0b\u987b\u77e5'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher_tell',
            field=models.CharField(blank=True, default='', max_length=200, null=True, verbose_name='\u8001\u5e08\u544a\u8bc9'),
        ),
    ]