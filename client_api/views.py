from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def register(request):
    """
    客户端注册api
    客户端将自己的静态信息，ip,主机名，等发送到接口，接口存入数据库
    """
    print(request.POST)
    return HttpResponse("ok")
