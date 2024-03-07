# Generated by Django 5.0.2 on 2024-03-05 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_profilelink_friendly_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='classes',
            field=models.ManyToManyField(blank=True, to='profiles.class'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='links',
            field=models.ManyToManyField(blank=True, to='profiles.profilelink'),
        ),
    ]