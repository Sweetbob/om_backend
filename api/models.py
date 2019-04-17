from django.db import models


# Create your models here.


class User(models.Model):
    """
    用户模型
    """
    username = models.CharField(max_length=32,primary_key=True)
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

