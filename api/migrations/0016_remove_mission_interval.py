# Generated by Django 2.1.7 on 2019-04-30 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_auto_20190430_1623'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mission',
            name='interval',
        ),
    ]
