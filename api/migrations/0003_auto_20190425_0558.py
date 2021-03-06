# Generated by Django 2.1.7 on 2019-04-25 05:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_cabinet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('ip', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('host_name', models.CharField(max_length=64)),
                ('cpu_model', models.CharField(max_length=64)),
                ('cpu_num', models.IntegerField()),
                ('memory', models.CharField(max_length=32)),
                ('disk', models.CharField(max_length=32)),
                ('system', models.CharField(max_length=32)),
                ('root', models.CharField(default='root', max_length=32)),
                ('password', models.CharField(default='123456', max_length=32)),
                ('cabinet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Cabinet')),
            ],
        ),
        migrations.AlterField(
            model_name='collective',
            name='machines',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Client'),
        ),
    ]
