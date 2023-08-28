# Generated by Django 3.2 on 2023-08-28 11:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_event_resource'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='link_uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
