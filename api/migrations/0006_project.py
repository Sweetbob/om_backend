# Generated by Django 2.1.7 on 2019-04-27 09:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_productline'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=32)),
                ('p_desc', models.CharField(max_length=1024)),
                ('language_type', models.IntegerField(choices=[(1, 'JAVA'), (2, 'php'), (3, 'Python'), (4, 'C#'), (5, 'Html'), (6, 'Javascript'), (7, 'C/C++'), (8, 'Ruby'), (9, 'Others')])),
                ('project_type', models.IntegerField(choices=[(1, '前端程序'), (2, '中间件'), (3, '后端程序')])),
                ('server_type', models.IntegerField(choices=[(1, 'Tomcat'), (2, 'WebLogic'), (3, 'Jetty'), (4, 'Nginx'), (5, 'Apache'), (6, 'Uwsgi'), (7, 'Others')])),
                ('app_frame', models.IntegerField(choices=[(1, 'Django'), (2, 'Flask'), (3, 'Tornado'), (4, 'Dubbo'), (5, 'Spring Boot'), (6, 'SSH'), (7, 'Spring Cloud'), (8, 'SSM'), (9, 'Others')])),
                ('warehouse_url', models.CharField(max_length=1024)),
                ('deploy_path', models.CharField(max_length=1024)),
                ('conf_path', models.CharField(max_length=1024)),
                ('charger', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.Charger')),
                ('productline', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.ProductLine')),
            ],
        ),
    ]
