# Generated by Django 2.1.7 on 2019-04-27 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='app_frame',
            field=models.IntegerField(choices=[(1, 'Django'), (2, 'Flask'), (3, 'Tornado'), (4, 'Dubbo'), (5, 'Spring Boot'), (6, 'SSH'), (7, 'Spring Cloud'), (8, 'SSM'), (9, 'Others')], null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='conf_path',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='deploy_path',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='language_type',
            field=models.IntegerField(choices=[(1, 'JAVA'), (2, 'php'), (3, 'Python'), (4, 'C#'), (5, 'Html'), (6, 'Javascript'), (7, 'C/C++'), (8, 'Ruby'), (9, 'Others')], null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='p_desc',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_type',
            field=models.IntegerField(choices=[(1, '前端程序'), (2, '中间件'), (3, '后端程序')], null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='server_type',
            field=models.IntegerField(choices=[(1, 'Tomcat'), (2, 'WebLogic'), (3, 'Jetty'), (4, 'Nginx'), (5, 'Apache'), (6, 'Uwsgi'), (7, 'Others')], null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='warehouse_url',
            field=models.CharField(max_length=1024, null=True),
        ),
    ]
