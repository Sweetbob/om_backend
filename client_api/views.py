from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from client_api.forms import ClientForm
from api.models import Client


@csrf_exempt
def register(request):
    """
    客户端注册api
    客户端将自己的静态信息，ip,主机名，等发送到接口，接口存入数据库
    """
    try:
        ip = request.POST.get('ip')
        client = Client.objects.filter(ip=ip).first()
        # 确保不重复注册
        if client:
            return HttpResponse('False')
        form_obj = ClientForm(request.POST)
        # 初次注册，且参数合理
        if form_obj.is_valid():
            form_obj.save()
            print('注册成功')
        return HttpResponse("True")
    except Exception as e:
        return HttpResponse("False")
