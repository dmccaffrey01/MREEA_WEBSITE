# Generated by Django 5.0.2 on 2024-03-26 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_remove_notification_status_remove_notification_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='cleared_status',
            field=models.BooleanField(default=False),
        ),
    ]