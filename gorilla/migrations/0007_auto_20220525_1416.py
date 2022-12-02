# Generated by Django 3.1.4 on 2022-05-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gorilla', '0006_auto_20220525_1311'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reportscheduledtask',
            options={'verbose_name': 'Gorilla Report - ScheduledTask', 'verbose_name_plural': 'Gorilla Report ScheduledTasks'},
        ),
        migrations.AlterField(
            model_name='reportscheduledtask',
            name='json',
            field=models.JSONField(blank=True, default='', verbose_name='Json'),
        ),
    ]