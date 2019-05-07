from django.db import models


# Create your models here.


class User(models.Model):
    """
    用户模型
    """
    username = models.CharField(max_length=32, primary_key=True)
    password = models.CharField(max_length=32)
    token = models.CharField(max_length=1024, null=True)


class Charger(models.Model):
    """
    运维人员模型
    """
    no = models.CharField(max_length=16)
    name = models.CharField(max_length=16)
    vocation = models.CharField(max_length=32)
    tel = models.CharField(max_length=16)
    email = models.CharField(max_length=32)




class Room(models.Model):
    """
    机房模型
    """
    no = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    machine_num = models.IntegerField(default=0)

    charger = models.ForeignKey(to=Charger, on_delete=models.SET_NULL, null=True, blank=True)


class Cabinet(models.Model):
    """
    机柜模型
    """
    no = models.CharField(max_length=16)
    name = models.CharField(max_length=32)
    address = models.CharField(max_length=64)
    machine_num = models.IntegerField()

    room = models.ForeignKey(to=Room, on_delete=models.SET_NULL, null=True, blank=True)


class Client(models.Model):
    """
    客户机静态模型
    """
    ip = models.CharField(max_length=32, primary_key=True)
    host_name = models.CharField(max_length=64)
    cpu_model = models.CharField(max_length=64)
    cpu_num = models.IntegerField()
    memory = models.CharField(max_length=32)
    disk = models.CharField(max_length=32)
    system = models.CharField(max_length=32)
    root = models.CharField(max_length=32, default='root')
    password = models.CharField(max_length=32, default='123456')
    cabinet = models.ForeignKey(to=Cabinet, on_delete=models.SET_NULL, null=True, blank=True)


class Collective(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=1024)
    machines = models.ManyToManyField(to=Client)


class SiteNavi(models.Model):
    site_name = models.CharField(max_length=32)
    site_address = models.CharField(max_length=1024)
    desc = models.CharField(max_length=32)


class AuthCenter(models.Model):
    host = models.CharField(max_length=32)
    ssh = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    port = models.IntegerField()
    ps = models.CharField(max_length=1024, null=True, default='', blank=True)


class Interval(models.Model):
    interval_amount = models.IntegerField()
    interval_measure = models.CharField(max_length=32)


class Crontab(models.Model):
    minute = models.CharField(max_length=32)
    hour = models.CharField(max_length=32)
    day_week = models.CharField(max_length=32)
    day_month = models.CharField(max_length=32)
    month_year = models.CharField(max_length=32)



class ProductLine(models.Model):
    name = models.CharField(max_length=32)
    desc = models.CharField(max_length=1024)
    charger = models.ForeignKey(to=Charger, on_delete=models.SET_NULL, null=True, blank=True)



class Project(models.Model):
    p_name = models.CharField(max_length=32)
    p_desc = models.CharField(max_length=1024, null=True, blank=True)
    language_type_choices = [
        (1, "JAVA"),
        (2, "php"),
        (3, "Python"),
        (4, "C#"),
        (5, "Html"),
        (6, "Javascript"),
        (7, "C/C++"),
        (8, "Ruby"),
        (9, "Others"),
    ]
    language_type = models.IntegerField(choices=language_type_choices, null=True, blank=True)
    project_type_choices = [
        (1, "前端程序"),
        (2, "中间件"),
        (3, "后端程序"),
    ]
    project_type = models.IntegerField(choices=project_type_choices, null=True, blank=True)
    server_type_choices = [
        (1, "Tomcat"),
        (2, "WebLogic"),
        (3, "Jetty"),
        (4, "Nginx"),
        (5, "Apache"),
        (6, "Uwsgi"),
        (7, "Others"),
    ]
    server_type = models.IntegerField(choices=server_type_choices, null=True, blank=True)
    app_frame_choices = [
        (1, "Django"),
        (2, "Flask"),
        (3, "Tornado"),
        (4, "Dubbo"),
        (5, "Spring Boot"),
        (6, "SSH"),
        (7, "Spring Cloud"),
        (8, "SSM"),
        (9, "Others"),
    ]
    app_frame = models.IntegerField(choices=app_frame_choices, null=True, blank=True)
    warehouse_type_choices = [(1,'SVN'), (2,'Git')]
    warehouse_type = models.IntegerField(choices=warehouse_type_choices, null=True, blank=True)
    warehouse_url = models.CharField(max_length=1024, null=True, blank=True)
    deploy_path = models.CharField(max_length=1024, null=True, blank=True)
    conf_path = models.CharField(max_length=1024, null=True, blank=True)
    productline = models.ForeignKey(to=ProductLine, blank=True, null=True, on_delete=models.SET_NULL)
    charger = models.ForeignKey(to=Charger, blank=True, null=True, on_delete=models.SET_NULL)


class Mission(models.Model):
    """
    mission
    """
    name = models.CharField(max_length=32)
    type = models.CharField(max_length=32)
    # interval = models.ForeignKey(to=Interval, on_delete=models.SET_NULL, null=True, blank=True)
    crontab = models.ForeignKey(to=Crontab, on_delete=models.SET_NULL, null=True, blank=True)
    content = models.CharField(max_length=1024)
    enabled = models.CharField(max_length=32)
    description = models.CharField(max_length=1024, null=True, blank=True)


class Cxfb(models.Model):
    deploy_type = models.CharField(max_length=32)
    if_clean = models.CharField(max_length=32, null=True, blank=True, default='0')
    if_local = models.CharField(max_length=32, null=True, blank=True, default='0')
    status = models.CharField(max_length=32, null=True, blank=True, default='未部署')
    shell = models.CharField(max_length=1024, null=True, blank=True, default='')
    project = models.ForeignKey(to=Project, on_delete=models.SET_NULL, null=True, blank=True)
    machines = models.ManyToManyField(to=Client)
