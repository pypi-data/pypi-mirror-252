# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-11-29 16:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("deposit", "0006_depositclient_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="depositclient",
            name="url",
            field=models.TextField(null=False),
        ),
    ]
