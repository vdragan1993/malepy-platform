# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-22 16:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('malepy', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='fake_testing',
            field=models.FileField(blank=True, null=True, upload_to='datasets/'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='testing',
            field=models.FileField(blank=True, null=True, upload_to='datasets/'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='training',
            field=models.FileField(blank=True, null=True, upload_to='datasets/'),
        ),
    ]
