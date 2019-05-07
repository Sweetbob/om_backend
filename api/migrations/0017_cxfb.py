# Generated by Django 2.1.7 on 2019-05-06 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_remove_mission_interval'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cxfb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deploy_type', models.CharField(max_length=32)),
                ('if_clean', models.CharField(max_length=32)),
                ('if_local', models.CharField(max_length=32)),
                ('shell', models.CharField(max_length=1024)),
                ('machines', models.ManyToManyField(to='api.Client')),
                ('project', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Project')),
            ],
        ),
    ]