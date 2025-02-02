# Generated by Django 3.2 on 2023-10-24 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=255)),
                ('description', models.TextField(blank=True, max_length=255, null=True)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('duration', models.IntegerField()),
                ('location', models.CharField(default='', max_length=255)),
            ],
        ),
    ]
