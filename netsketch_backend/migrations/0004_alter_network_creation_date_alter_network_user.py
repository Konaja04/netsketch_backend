# Generated by Django 4.2.19 on 2025-02-26 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netsketch_backend', '0003_remove_network_creation_ate_network_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='network',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='network',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
