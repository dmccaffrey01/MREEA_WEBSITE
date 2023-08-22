# Generated by Django 3.2 on 2023-08-22 13:16

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0024_remove_memberprofile_short_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='event_image',
            field=cloudinary.models.CloudinaryField(blank=True, default='https://res.cloudinary.com/dzwyiggcp/image/upload/v1689582480/MREEA/mreea-meeting-2_adho8o.png', max_length=255, null=True, verbose_name='Event Image'),
        ),
        migrations.AddField(
            model_name='event',
            name='event_image_change',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]
