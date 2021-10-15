# Generated by Django 3.2.6 on 2021-08-09 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rconc', '0013_auto_20210809_1010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Code',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('script_name', models.CharField(max_length=200, verbose_name='コードの名前')),
                ('selecter', models.CharField(choices=[('1', 'Active'), ('2', 'Inactive')], default='2', max_length=1, verbose_name='実行の形式')),
                ('condition', models.CharField(choices=[('1', '1分おきに実行する'), ('2', '1秒おきに実行する')], default='1', max_length=10)),
                ('code', models.TextField(verbose_name='コード')),
            ],
        ),
    ]