# Generated by Django 5.0.2 on 2024-05-21 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0020_alter_userprofile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilelink',
            name='url',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
