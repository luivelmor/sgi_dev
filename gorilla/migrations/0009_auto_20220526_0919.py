# Generated by Django 3.1.4 on 2022-05-26 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gorilla', '0008_auto_20220526_0914'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reporttype',
            name='type',
        ),
        migrations.AddField(
            model_name='reporttype',
            name='name',
            field=models.CharField(default='not defined', max_length=100, verbose_name='Name'),
        ),
    ]