# Generated by Django 3.1.4 on 2022-05-25 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gorilla', '0005_reportscheduledtask_manifest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportscheduledtask',
            name='manifest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='manifest_gorilla_report_scheduled_task', to='gorilla.manifest', verbose_name='Manifest'),
        ),
    ]
