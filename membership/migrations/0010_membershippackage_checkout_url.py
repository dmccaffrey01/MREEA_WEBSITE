# Generated by Django 5.0.2 on 2024-02-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0009_membershippackage_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershippackage',
            name='checkout_url',
            field=models.URLField(default='https://next.waveapps.com/checkouts/c2bfa0b20008412ba69c845cd92834d3'),
            preserve_default=False,
        ),
    ]
