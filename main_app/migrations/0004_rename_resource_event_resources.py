# Generated by Django 3.2 on 2023-08-28 12:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_resource_link_uuid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='resource',
            new_name='resources',
        ),
    ]
