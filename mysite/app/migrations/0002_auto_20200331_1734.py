# Generated by Django 3.0.4 on 2020-03-31 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='date_start',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='time_start',
        ),
    ]