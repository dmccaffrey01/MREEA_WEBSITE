# Generated by Django 5.0.2 on 2024-03-29 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='annoucement',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
