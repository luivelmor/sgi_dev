# Generated by Django 3.1.4 on 2021-12-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0018_delete_invoicedevice'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='serialNumber',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Serial'),
        ),
    ]
