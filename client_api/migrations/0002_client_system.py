# Generated by Django 2.1.7 on 2019-04-17 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client_api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='system',
            field=models.CharField(default='centos', max_length=32),
            preserve_default=False,
        ),
    ]