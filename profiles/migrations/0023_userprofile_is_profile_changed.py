# Generated by Django 5.0.6 on 2024-11-27 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0022_alter_userprofile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_profile_changed',
            field=models.BooleanField(default=True),
        ),
    ]
