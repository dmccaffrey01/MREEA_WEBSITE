# Generated by Django 3.2 on 2023-07-25 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_memberprofile_profile_image_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='memberprofile',
            old_name='profile_image_url',
            new_name='profile_image_change',
        ),
    ]