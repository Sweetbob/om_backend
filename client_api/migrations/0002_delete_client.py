# Generated by Django 2.1.7 on 2019-04-25 05:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190425_0558'),
        ('client_api', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Client',
        ),
    ]
