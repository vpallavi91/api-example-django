# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 18:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drchrono', '0002_patientmodel_msgtext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patientmodel',
            name='msgtext',
        ),
    ]