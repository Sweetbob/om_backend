from django.db import models

# Create your models here.
from api.models import Cabinet


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
    cabinet = models.ForeignKey(to=Cabinet, on_delete=models.SET_NULL, null=True, blank=True)





