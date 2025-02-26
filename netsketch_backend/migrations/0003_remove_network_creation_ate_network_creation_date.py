# Generated by Django 4.2.19 on 2025-02-26 13:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netsketch_backend', '0002_device_routingtable_network_interface_device_network_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='network',
            name='creation_ate',
        ),
        migrations.AddField(
            model_name='network',
            name='creation_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
