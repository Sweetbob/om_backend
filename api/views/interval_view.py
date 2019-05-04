from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import IntervalForm
from api.models import Interval
from api.serializers import IntervalModelSerializer
from api.utils.auth_util import check_login


class IntervalView(APIView):

    def get(self, request):
        """
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        print('interval get')
        intervals = Interval.objects.all()

        data = IntervalModelSerializer(instance=intervals, many=True)
        print(data.data)

        result['data'] = data.data
        return Response(data=result)

    #
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

        # 添加机房
        new_i = IntervalForm(request.data)
        print(request.data)
        if new_i.is_valid():
            i_obj = new_i.save()
            result['data'] = IntervalModelSerializer(instance=i_obj, many=False).data
            return Response(data=result)
        else:
            print(new_i.errors)
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
        Interval.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)

