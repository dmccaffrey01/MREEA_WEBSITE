# Generated by Django 3.2 on 2023-08-21 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0023_alter_memberprofile_short_bio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='short_bio',
        ),
    ]
