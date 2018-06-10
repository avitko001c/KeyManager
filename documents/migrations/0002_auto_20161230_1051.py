# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-30 10:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='original_filename',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AlterField(
            model_name='document',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='documents.Folder'),
        ),
    ]
