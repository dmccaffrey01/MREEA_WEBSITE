# Generated by Django 5.0.6 on 2024-05-31 15:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0028_alter_membershipupdatestatus_name'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MembershipUpdateStatus',
        ),
    ]
