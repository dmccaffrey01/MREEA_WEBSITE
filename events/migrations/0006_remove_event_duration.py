# Generated by Django 5.0.2 on 2024-05-21 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_remove_event_registration_link_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='duration',
        ),
    ]
