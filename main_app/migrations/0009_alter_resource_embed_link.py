# Generated by Django 3.2 on 2023-08-29 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_resource_embed_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='embed_link',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
    ]
