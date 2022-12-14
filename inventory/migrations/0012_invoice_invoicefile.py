# Generated by Django 3.1.4 on 2021-12-02 08:56

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0011_devicemodel_alias'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('warranty_from', models.DateTimeField(verbose_name='Warranty from')),
                ('warranty_to', models.DateTimeField(verbose_name='Warranty to')),
                ('notes', ckeditor.fields.RichTextField(blank=True, default='', max_length=500, verbose_name='Notes')),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.device', verbose_name='Device Invoice')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='InvoiceFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=150, verbose_name='Filename')),
                ('file', models.FileField(upload_to=inventory.models.PathAndRename('inventory/invoice_files'), verbose_name='File')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.invoice', verbose_name='Invoice')),
            ],
            options={
                'verbose_name': 'Invoice file',
                'verbose_name_plural': 'Invoice files',
            },
        ),
    ]
