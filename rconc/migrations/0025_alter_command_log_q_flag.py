# Generated by Django 3.2.6 on 2021-09-29 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rconc', '0024_alter_command_log_q_flag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command_log',
            name='q_flag',
            field=models.BooleanField(default=False),
        ),
    ]