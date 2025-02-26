# Generated by Django 4.2.19 on 2025-02-26 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netsketch_backend', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('image', models.TextField()),
                ('type', models.CharField(choices=[('router', 'Router'), ('switch', 'Switch'), ('pc', 'PC')], max_length=10)),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RoutingTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destiny', models.GenericIPAddressField()),
                ('destiny_mask', models.GenericIPAddressField()),
                ('jump', models.GenericIPAddressField()),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='netsketch_backend.device')),
            ],
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('creation_ate', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='networks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interface',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('ip', models.GenericIPAddressField(blank=True, null=True)),
                ('mask', models.GenericIPAddressField(blank=True, null=True)),
                ('gateway', models.GenericIPAddressField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='interfaces', to='netsketch_backend.device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='devices', to='netsketch_backend.network'),
        ),
        migrations.CreateModel(
            name='Cable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_interface', models.CharField(max_length=50)),
                ('from_x', models.IntegerField()),
                ('from_y', models.IntegerField()),
                ('to_interface', models.CharField(max_length=50)),
                ('to_x', models.IntegerField()),
                ('to_y', models.IntegerField()),
                ('weight', models.IntegerField()),
                ('from_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cables_salida', to='netsketch_backend.device')),
                ('to_device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cables_entrada', to='netsketch_backend.device')),
            ],
        ),
    ]
