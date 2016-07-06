# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-06 08:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_identifier', models.CharField(max_length=20)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('create_ip', models.CharField(max_length=39)),
                ('referrer', models.CharField(blank=True, max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=150)),
                ('extension', models.CharField(blank=True, max_length=3)),
                ('identifier', models.CharField(max_length=20, unique=True)),
                ('create_date', models.DateTimeField(verbose_name='date published')),
                ('create_ip', models.CharField(max_length=39)),
            ],
        ),
    ]