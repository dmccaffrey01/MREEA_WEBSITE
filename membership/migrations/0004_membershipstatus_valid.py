# Generated by Django 5.0.2 on 2024-02-13 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0003_membershipstatus_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershipstatus',
            name='valid',
            field=models.BooleanField(default=False),
        ),
    ]
