# Generated by Django 3.1.4 on 2021-05-14 05:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gorilla', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventlog',
            name='details',
            field=ckeditor.fields.RichTextField(blank=True, default='', max_length=100, verbose_name='Details'),
        ),
    ]
