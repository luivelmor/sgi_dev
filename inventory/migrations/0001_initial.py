# Generated by Django 3.1.4 on 2021-05-07 10:39

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import inventory.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', ckeditor.fields.RichTextField(blank=True, default='', max_length=500, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Device',
                'verbose_name_plural': 'Devices',
            },
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True, verbose_name='Name')),
                ('image', models.ImageField(blank=True, default='inventory/deviceModel_images/default.png', upload_to=inventory.models.PathAndRename('inventory/deviceModel_images'), verbose_name='Image')),
                ('notes', ckeditor.fields.RichTextField(blank=True, default='', max_length=500, verbose_name='Notes')),
            ],
            options={
                'verbose_name': 'Device model',
                'verbose_name_plural': 'Device models',
                'ordering': ('deviceType', 'name'),
            },
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=25, unique=True, verbose_name='Name')),
            ],
            options={
                'verbose_name': 'Device type',
                'verbose_name_plural': 'Device types',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='DriverFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=150, verbose_name='Filename')),
                ('file', models.FileField(upload_to=inventory.models.PathAndRename('inventory/driverFile_files'), verbose_name='File')),
            ],
            options={
                'verbose_name': 'Driver file',
                'verbose_name_plural': 'Drivers files',
            },
        ),
        migrations.CreateModel(
            name='ModificationRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField(default='', max_length=1000, verbose_name='Text')),
                ('verified', models.BooleanField(blank=True, default=False, verbose_name='Verified')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='added_by', to=settings.AUTH_USER_MODEL, verbose_name='Added by')),
                ('verified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Verified by')),
            ],
            options={
                'verbose_name': 'Modification request',
                'verbose_name_plural': 'Modification requests',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True, verbose_name='Name')),
                ('floor', models.CharField(choices=[('Planta 0', 'Planta 0'), ('Planta 1', 'Planta 1'), ('Planta 2', 'Planta 2'), ('Planta 3', 'Planta 3'), ('Planta 4', 'Planta 4')], max_length=100, verbose_name='Floor')),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=100, unique=True, verbose_name='Name')),
                ('room', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.room', verbose_name='Room')),
            ],
            options={
                'verbose_name': 'Place',
                'verbose_name_plural': 'Places',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='ModificationRequestFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=150, verbose_name='Filename')),
                ('file', models.FileField(upload_to=inventory.models.PathAndRename('inventory/deviceModel_files'), verbose_name='File')),
                ('modificationRequest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.modificationrequest', verbose_name='Modification request')),
            ],
            options={
                'verbose_name': 'Modification request file',
                'verbose_name_plural': 'Modification request files',
            },
        ),
        migrations.CreateModel(
            name='MicrophoneFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequency', models.CharField(blank=True, default='', max_length=100, verbose_name='Frequency')),
                ('channel', models.CharField(blank=True, default='', max_length=100, verbose_name='Channel')),
                ('room', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.room', verbose_name='Room')),
            ],
            options={
                'verbose_name': 'Microphone frequency',
                'verbose_name_plural': 'Microphone frequencies',
                'ordering': ('room',),
            },
        ),
        migrations.CreateModel(
            name='DevicePlace',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='inventory.device', verbose_name='Device')),
                ('place', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.place', verbose_name='Place')),
            ],
            options={
                'verbose_name': 'DevicePlace',
                'verbose_name_plural': 'DevicesPlaces',
            },
        ),
        migrations.CreateModel(
            name='DeviceModelFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(default='', max_length=150, verbose_name='Filename')),
                ('file', models.FileField(upload_to=inventory.models.PathAndRename('inventory/deviceModel_files'), verbose_name='File')),
                ('deviceModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.devicemodel', verbose_name='Device model')),
            ],
            options={
                'verbose_name': 'Device model file',
                'verbose_name_plural': 'Device model files',
            },
        ),
        migrations.CreateModel(
            name='DeviceModelDriverFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deviceModel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.devicemodel', verbose_name='Device model')),
                ('driverFile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.driverfile', verbose_name='Driver file')),
            ],
            options={
                'verbose_name': 'Device model driver file',
                'verbose_name_plural': 'Device models drivers files',
            },
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='deviceType',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.devicetype', verbose_name='Device type'),
        ),
        migrations.AddField(
            model_name='device',
            name='deviceModel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.devicemodel', verbose_name='Device model'),
        ),
        migrations.AddField(
            model_name='device',
            name='room',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='inventory.room', verbose_name='Room'),
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
            ],
            options={
                'verbose_name': 'Store',
                'verbose_name_plural': 'Store',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('inventory.devicemodel',),
        ),
    ]