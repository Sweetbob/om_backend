# Generated by Django 2.1.7 on 2019-04-25 05:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Charger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=16)),
                ('vocation', models.CharField(max_length=32)),
                ('tel', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Collective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
                ('desc', models.CharField(max_length=1024)),
                ('machines', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='client_api.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=32)),
                ('address', models.CharField(max_length=64)),
                ('machine_num', models.IntegerField(default=0)),
                ('charger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Charger')),
            ],
        ),
        migrations.CreateModel(
            name='SiteNavi',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=32)),
                ('site_address', models.CharField(max_length=1024)),
                ('desc', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=32)),
                ('token', models.CharField(max_length=1024, null=True)),
            ],
        ),
    ]
