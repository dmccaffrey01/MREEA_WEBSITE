# Generated by Django 5.0.2 on 2024-02-13 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0006_alter_membership_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
