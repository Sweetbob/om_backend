from django.db import models

# Create your models here.


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
