# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-22 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('officialexam', '0002_auto_20181022_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='granted_wish',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
