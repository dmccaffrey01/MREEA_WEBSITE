# Generated by Django 3.2 on 2023-07-25 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_memberprofile_cropping'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='memberprofile',
            name='cropping',
        ),
    ]
