# Generated by Django 3.1.4 on 2021-05-14 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0009_auto_20210514_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(default='#b70505', max_length=20, verbose_name='Color'),
        ),
    ]