# Generated by Django 4.2.19 on 2025-02-26 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netsketch_backend', '0004_alter_network_creation_date_alter_network_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routingtable',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='routing_tables', to='netsketch_backend.device'),
        ),
    ]
