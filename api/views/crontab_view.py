from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import CrontabForm
from api.models import Crontab
from api.serializers import CrontabModelSerializer
from api.utils.auth_util import check_login


class CrontabView(APIView):

    def get(self, request):
        """
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        crontabs = Crontab.objects.all()

        data = CrontabModelSerializer(instance=crontabs, many=True)
        print(data.data)

        result['data'] = data.data
        return Response(data=result)


    def post(self, request):
        """
        添加interval
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        print(request.query_params.get('token'))
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        new_c = CrontabForm(request.data)
        print(request.data)
        if new_c.is_valid():
            c_obj = new_c.save()
            result['data'] = CrontabModelSerializer(instance=c_obj, many=False).data
            return Response(data=result)
        else:
            print(new_c.errors)
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
        Crontab.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)

