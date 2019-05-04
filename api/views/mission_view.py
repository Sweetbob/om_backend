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
    # if job is not created
    id_name = str(mission.id) + "_" + mission.name
    objs = my_user_cron.find_comment(id_name)
    print(my_user_cron.crons)
    if len(my_user_cron.crons):
        print('xxx')
    else:
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
    # except Exception as e:
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)