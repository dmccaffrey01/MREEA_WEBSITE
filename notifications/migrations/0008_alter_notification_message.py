# Generated by Django 5.0.2 on 2024-05-03 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_delete_notificationcategory_notification_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.TextField(max_length=3000),
        ),
    ]
