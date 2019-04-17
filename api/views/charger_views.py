from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import ChargerForm
from api.models import Charger
from api.serializers import ChargerModelSerializer
from api.utils.auth_util import check_login


class ChargerView(APIView):

    def get(self, request):
        """
        获取所有运维人员
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 返回人员数据
            charger_data = ChargerModelSerializer(instance=Charger.objects.all(), many=True)

            result['data'] = charger_data.data
            return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def post(self, request):
        """
        添加运维人员
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 添加运维人员
            new_charger = ChargerForm(request.data)
            if new_charger.is_valid():
                charger = new_charger.save()
                result['data'] = ChargerModelSerializer(instance=charger, many=False).data
                return Response(data=result)
            else:
                result['code'] = 1001
                request['error'] = 'field not valid!'
                return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def put(self, request):
        """
        修改运维人员
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 修改运维人员
            charger_from_db = Charger.objects.filter(pk=request.data.get('id')).first()
            edit_charger = ChargerForm(request.data, instance=charger_from_db)
            if edit_charger.is_valid():
                edited_charger = edit_charger.save()
                result['data'] = ChargerModelSerializer(instance=edited_charger, many=False).data
                return Response(data=result)
            else:
                result['code'] = 1001
                request['error'] = 'field not valid!'
                return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def delete(self, request):
        """
        删除运维人员
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 删除运维人员
            Charger.objects.filter(pk=request.query_params.get("id")).delete()
            return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)
