# Generated by Django 5.0.2 on 2024-02-27 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0002_resource_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
    ]
