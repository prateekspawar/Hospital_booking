# Generated by Django 3.0.4 on 2020-03-31 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20200331_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='patient_mob',
            field=models.CharField(default='1234567890', max_length=10),
        ),
        migrations.AddField(
            model_name='booking',
            name='patient_name',
            field=models.CharField(default='patient_name', max_length=200),
        ),
    ]