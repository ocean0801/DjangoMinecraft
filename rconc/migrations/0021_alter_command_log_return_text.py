# Generated by Django 3.2.5 on 2021-08-29 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rconc', '0020_command_log'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command_log',
            name='return_text',
            field=models.CharField(max_length=100, verbose_name='実行結果'),
        ),
    ]