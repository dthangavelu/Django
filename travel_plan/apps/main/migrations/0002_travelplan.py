# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-25 14:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('travel_start_date', models.DateTimeField(auto_now=True)),
                ('travel_end_date', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now)),
                ('joined_users', models.ManyToManyField(related_name='joined_travels', to='main.User')),
                ('travel_panned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='planned_travel', to='main.User')),
            ],
        ),
    ]