# Generated by Django 3.2.6 on 2021-08-10 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rconc', '0016_auto_20210810_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='rq',
            field=models.CharField(choices=[('1', 'Rcon'), ('2', 'Query')], default='1', max_length=10, verbose_name='Rcon/Query'),
        ),
        migrations.AlterField(
            model_name='code',
            name='selecter',
            field=models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default='2', max_length=1, verbose_name='状態'),
        ),
    ]
