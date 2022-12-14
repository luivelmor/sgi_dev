# Generated by Django 3.1.4 on 2022-06-20 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0019_device_serialnumber'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deviceplace',
            name='tags',
            field=models.ManyToManyField(blank=True, to='inventory.Tag'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='devices',
            field=models.ManyToManyField(blank=True, to='inventory.Device', verbose_name='Devices'),
        ),
    ]
