# Generated by Django 3.2.6 on 2021-09-29 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rconc', '0023_auto_20210929_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command_log',
            name='q_flag',
            field=models.BooleanField(default=False, verbose_name=''),
        ),
    ]