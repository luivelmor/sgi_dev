# Generated by Django 3.1.4 on 2021-12-15 08:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0017_invoice_devices'),
    ]

    operations = [
        migrations.DeleteModel(
            name='InvoiceDevice',
        ),
    ]
