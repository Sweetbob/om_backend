import json
import os
import time

import pexpect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User, Room, Cabinet
from api.utils.auth_util import check_login
from api.utils.network_util import is_alive
from api.utils.redis_util import redis_client
from client_api.forms import ClientForm
from api.models import Client
from client_api.serializers import ClientSerializer


class ClientStaticView(APIView):

    def get(self, request):
        """
        获取所有主机的静态信息
        """
        result = {"code": "1000"}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        # 返回主机静态数据
        client_list = Client.objects.all()
        client_data = ClientSerializer(instance=client_list, many=True)
        for item in client_data.data:
            item['status'] = '检测中...'
        result['data'] = client_data.data
        return Response(data=result)

    def put(self, request):
        """
        修改主机数据，事实上只修改一个机柜
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 修改主机
        client_from_db = Client.objects.filter(pk=request.data.get('ip')).first()
        edit_client = ClientForm(request.data, instance=client_from_db)
        if edit_client.is_valid():
            edited_client = edit_client.save()
            result['data'] = ClientSerializer(instance=edited_client, many=False).data
            return Response(data=result)
        else:
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def delete(self, request):
        """
        删除主机
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 删除主机
        Client.objects.filter(pk=request.query_params.get("ip")).delete()
        return Response(data=result)


@api_view(('GET',))
def client_extra_num(request):
    """
    获取主机数
    """
    result = {"code": "1000"}
    print('Laile ')
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        # 返回主机数
        client_num = Client.objects.all().count()
        result['data'] = {"num": client_num}
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def room_extra_num(request):
    """
    获取room数
    """
    result = {"code": "1000"}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        # 返回主机数
        room_num = Room.objects.all().count()
        result['data'] = {"num": room_num}
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def cabinet_extra_num(request):
    """
    获取cabinet数
    """
    result = {"code": "1000"}
    print('Laile ')
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        # 返回主机数
        cabinet_num = Cabinet.objects.all().count()
        result['data'] = {"num": cabinet_num}
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def client_detail(request):
    """
    获取主机detail
    """
    result = {"code": "1000"}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)

    # 返回detail
    ip = request.query_params.get('ip')
    client = Client.objects.all().filter(ip=ip).first()
    result['data'] = ClientSerializer(instance=client, many=False).data
    return Response(data=result)


@api_view(('POST',))
def change_pw(request):

    result = {"code": "1000"}

    user = request.data.get("user")
    old_pw = request.data.get("oldpw")
    newpw = request.data.get("newpw")
    print(user)
    print(old_pw)
    print(newpw)
    user = User.objects.filter(username=user, password=old_pw).first()
    if not user:
        result['code'] = "1001"
        result['error'] = "旧密码不对"
        return Response(data=result)
    # 返回detail
    user.password = newpw
    user.save()
    return Response(data=result)


@api_view(('GET',))
def client_poweroff(request):
    """
    关机
    """
    result = {"code": "1000"}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    print(ip)
    # 执行关机命令
    result['data'] = os.system("ssh root@" + ip + " poweroff")
    time.sleep(10)
    return Response(data=result)


@api_view(('GET',))
def client_reboot(request):
    """
    reboot
    """
    result = {"code": "1000"}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    # 执行reboot命令
    result['data'] = os.system("ssh root@" + ip + " reboot")
    time.sleep(30)
    return Response(data=result)



@api_view(('GET',))
def ping(request):
    """
    ping 主机
    """
    ip = request.query_params.get("ip")
    result = {"code": "1000"}
    print('laile' + ip)
    if is_alive(ip=ip):
        result['status'] = "运行中"
    else:
        result['status'] = "已停止"
    return Response(data=result)

@api_view(('GET',))
def machine_num_by_type(request):
    """
    """
    result = {"code": "1000"}
    running_machine = 0
    stopped_machine = 0
    for c in Client.objects.all():
        if is_alive(ip=c.ip):
            running_machine += 1
        else:
            stopped_machine += 1
    result['data'] = {
        "running_machine": running_machine,
        "stopped_machine": stopped_machine,
    }
    return Response(data=result)



@api_view(('GET',))
def current_realtime_info(request):
    """
    ger newest realtime info
    """
    result = {"code": "1000"}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)
        ip = request.query_params.get('ip')
        newest_data = redis_client.lindex(ip, -1)
        result['data'] = newest_data
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def realtime_infos(request):
    """
    ger realtime info
    """
    result = {"code": "1000"}
    # try:
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    data = redis_client.lrange(ip, 0, -1)
    xAxis = []
    cpu_value = []

    disk_value = []
    mem_value = []
    process_value = []
    for item in data:
        xAxis.append(json.loads(item).get("time"))
        cpu_value.append(json.loads(item).get("cpu_1"))
        mem_value.append(json.loads(item).get("memory_used"))
        process_value.append(json.loads(item).get("processes"))
        disk_value.append(str(json.loads(item).get("disk_available")).replace("G", ""))
    data = {
        "xAxis": xAxis,
        "cpu_value": cpu_value,
        "disk_value": disk_value,
        "mem_value": mem_value,
        "process_value": process_value,
    }
    result['data'] = data
    return Response(data=result)
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)


@api_view(('GET',))
def client_of_cabinet(request):
    """
    获取 cclient_of_cabinet
    """
    result = {"code": "1000"}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)

    # 返回detail
    id = request.query_params.get('id')
    clients = Client.objects.filter(cabinet_id=id).all()

    result['data'] = ClientSerializer(instance=clients, many=True).data
    return Response(data=result)


@api_view(('GET',))
def firewall_status(request):
    """
    ger the status of this ip
    """
    result = {"code": "1000", 'data': ""}
    # try:
        # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    command = "firewall-cmd --state"
    ssh = pexpect.spawn('ssh %s@%s "%s"' % ('root', ip, command))
    if b"not" in ssh.read():
        status = "关"
    else:
        status = "开"
    result['data'] = {
        'status': status
    }
    return Response(data=result)
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)


@api_view(('GET',))
def firewall_changing(request):
    """
    ger the status of this ip
    """
    result = {"code": "1000", 'data': ""}
    # try:
        # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    flag = request.query_params.get('flag')
    if flag == "0":
        # stop
        os.popen('ssh %s@%s "%s"' % ('root', ip, 'systemctl stop firewalld'))
    else:
        # start
        os.popen('ssh %s@%s "%s"' % ('root', ip, 'systemctl start firewalld'))
    time.sleep(5)
    command = "firewall-cmd --state"
    ssh = pexpect.spawn('ssh %s@%s "%s"' % ('root', ip, command))
    if b"not" in ssh.read():
        status = "关"
    else:
        status = "开"
    result['data'] = {
        'status': status
    }
    return Response(data=result)
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)


@api_view(('GET',))
def host_name_changing(request):
    """
    change host_name
    """
    result = {"code": "1000", 'data': ""}
    # try:
        # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    ip = request.query_params.get('ip')
    host_name = request.query_params.get('host_name')
    os.popen('ssh %s@%s "%s"' % ('root', ip, 'hostname ' + host_name))
    os.popen('ssh %s@%s "%s"' % ('root', ip, 'echo ' + host_name + ' > /etc/hostname'))
    client = Client.objects.filter(ip=ip).first()
    client.host_name = host_name
    client.save()
    result['data'] = ClientSerializer(instance=client, many=False).data
    return Response(data=result)
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)
