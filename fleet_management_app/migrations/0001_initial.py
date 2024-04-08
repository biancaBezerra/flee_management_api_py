# Generated by Django 5.0.4 on 2024-04-08 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Taxi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('plate', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trajectory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('taxi_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trajectories', to='fleet_management_app.taxi')),
            ],
        ),
    ]