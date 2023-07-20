# Generated by Django 3.2 on 2023-07-17 11:37

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='unique_event_id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=200),
        ),
    ]