import os
import time

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import MissionForm
from api.models import Mission
from api.serializers import MissionSerializer
from api.utils.auth_util import check_login

from crontab import CronTab


class MissionView(APIView):
    def get(self, request):
        """
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        missions = Mission.objects.all()

        data = MissionSerializer(instance=missions, many=True)
        print(data.data)

        result['data'] = data.data
        return Response(data=result)

    def put(self, request):
        """
        修改mission
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            # 修改
            m_from_db = Mission.objects.filter(pk=request.data.get('id')).first()
            edit_m = MissionForm(request.data, instance=m_from_db)
            print(request.data)
            if edit_m.is_valid():
                edited_m = edit_m.save()
                result['data'] = MissionSerializer(instance=edited_m, many=False).data
                return Response(data=result)
            else:
                result['code'] = 1001
                request['error'] = 'field not valid!'
                return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def post(self, request):
        """
        添加
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        print(request.query_params.get('token'))
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        new_m = MissionForm(request.data)
        print(request.data)
        if new_m.is_valid():
            m = new_m.save()
            return Response(data=result)
        else:
            print(new_m.errors)
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def delete(self, request):
        """
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 删除机房
        Mission.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)


@api_view(('GET',))
def start_mission(request):
    """
    start mission
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

        id = request.query_params.get('id')
        my_user_cron = CronTab(user=True)
        mission = Mission.objects.filter(pk=id).first()
        # if job is not created
        id_name = str(mission.id) + "_" + mission.name
        wrap_content = mission.content + " >> /opt/log/" + id_name + ".log"
        print(wrap_content)
        job = my_user_cron.new(command=wrap_content)
        # 设置任务执行周期
        crontab = mission.crontab
        crontab_str = crontab.minute + " " + crontab.hour + " " + crontab.day_week + " " + crontab.day_month + " " \
                      + crontab.month_year
        job.setall(crontab_str)
        job.set_comment(id_name)
        job.enable()
        my_user_cron.write()
        mission.enabled = '1'
        mission.save()
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def stop_mission(request):
    """
    stop mission
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

    id = request.query_params.get('id')
    my_user_cron = CronTab(user=True)
    mission = Mission.objects.filter(pk=id).first()
    id_name = str(mission.id) + "_" + mission.name
    for job in my_user_cron.crons:
        if job.comment == id_name:
            my_user_cron.remove(job)
    my_user_cron.write()

    mission.enabled = '0'
    mission.save()
    return Response(data=result)
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)


@api_view(('GET',))
def mission_log(request):
    """
    get mission log
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        id = request.query_params.get('id')
        mission = Mission.objects.filter(pk=id).first()
        updated_time = ''
        log = ""
        file_name = "/opt/log/" + str(mission.id) + "_" + mission.name + ".log"
        try:

            with open(file_name) as log_file:
                log = log_file.read()
            updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(file_name).st_ctime))
            print(updated_time)
        except Exception:
            print('error')
        result['data'] = {
            "log": log,
            "updated_time": updated_time,
            'mission_name': mission.name
        }

        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('POST',))
def execute_shell(request):
    """
    mission-executing view
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        my_file = '/opt/log/shell_log/last_rest.log'
        if os.path.exists(my_file):
            os.remove(my_file)

        ips = request.data.get('ips')
        command = request.data.get('command')
        args = request.data.get('args')
        for ip in ips:
            command_temp = 'ssh root@' + ip + " '" + command + " " + args + "' " + ">> /opt/log/shell_log/last_result.log"
            print(command_temp)
            os.system(command_temp)
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def shell_log(request):
    """
    get shell log
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        file_name = "/opt/log/shell_log/last_result.log"
        log = ''
        updated_time = ''
        try:

            with open(file_name) as log_file:
                log = log_file.read()
            updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(file_name).st_ctime))
        except Exception:
            print('error')
        result['data'] = {
            "log": log,
            "updated_time": updated_time,
        }

        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('POST',))
def execute_playbook(request):
    """
    mission-executing view
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        playbook = request.data.get('play_book')
        os.system('ansible-playbook /opt/ansible/playbook/'+playbook + " > /opt/log/ansible_playbook.log")
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('POST',))
def execute_ansible_command(request):
    """
    mission-executing view
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        ips = request.data.get('ips')
        command = request.data.get('command')
        print(ips)
        print(command)
        open('/etc/ansible/test', 'w').close()
        f = open('/etc/ansible/test', 'a')
        f.write('[default]')
        for ip in ips:
            f.write('\n'+ip)
        f.close()
        os.system("ansible default -i /etc/ansible/test -m command -a '" + command + "' > /opt/log/ansible_command.log")
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)

@api_view(('GET',))
def get_playbook(request):
    """
    get playbook
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)
        f_list = os.listdir('/opt/ansible/playbook/')
        pbs = []
        # print f_list
        for i in f_list:
            # os.path.splitext():分离文件名与扩展名
            if os.path.splitext(i)[1] == '.yml':
                pbs.append(i)
        result['data'] = pbs
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)




@api_view(('GET',))
def ansible_log(request):
    """
    get ansible log
    """
    result = {"code": "1000", 'data': ''}
    try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result = {
                "code": "1001",
                'error': 'not valid token!'
            }
            return Response(data=result)

        c_file_name = "/opt/log/ansible_command.log"
        p_file_name = "/opt/log/ansible_playbook.log"
        c_log = ''
        p_log = ''
        c_updated_time = ''
        p_updated_time = ''
        try:
            with open(c_file_name) as c:
                c_log = c.read()
            c_updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(c_file_name).st_ctime))
            with open(p_file_name) as p:
                p_log = p.read()
            p_updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(p_file_name).st_ctime))
        except Exception:
            print('error')
        result['data'] = {
            "c_log": c_log,
            "c_updated_time": c_updated_time,
            "p_log": p_log,
            "p_updated_time": p_updated_time,
        }

        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)
