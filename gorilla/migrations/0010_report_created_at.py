# Generated by Django 3.1.4 on 2022-05-26 09:15

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('gorilla', '0009_auto_20220526_0919'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Created at'),
            preserve_default=False,
        ),
    ]
