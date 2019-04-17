from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import CabinetForm
from api.models import Cabinet
from api.serializers import CabinetSerializer
from api.utils.auth_util import check_login
from client_api.models import Client


class CabinetView(APIView):

    def get(self, request):
        """
        获取所有机柜
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 返回机柜数据
        cabinets = Cabinet.objects.all()
        for r in cabinets:
            # 计算每个机柜的主机数
            r.machine_num = Client.objects.filter(cabinet=r.pk).count()
            r.save()
        cabinets_data = CabinetSerializer(instance=cabinets, many=True)
        print(cabinets_data.data)

        result['data'] = cabinets_data.data
        return Response(data=result)
        # except Exception as e:
        #     result['code'] = '1001'
        #     result['error'] = 'some unknown error!'
        #     return Response(data=result)

    def post(self, request):
        """
        添加机柜
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 添加机房
        new_cabinet = CabinetForm(request.data)
        print(request.data)
        if new_cabinet.is_valid():
            cabinet = new_cabinet.save()
            result['data'] = CabinetSerializer(instance=cabinet, many=False).data
            return Response(data=result)
        else:
            print(new_cabinet.errors)
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def put(self, request):
        """
        修改机柜
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 修改机柜
        cabinet_from_db = Cabinet.objects.filter(pk=request.data.get('id')).first()
        edit_cabinet = CabinetForm(request.data, instance=cabinet_from_db)
        if edit_cabinet.is_valid():
            edited_cabinet = edit_cabinet.save()
            result['data'] = CabinetSerializer(instance=edited_cabinet, many=False).data
            return Response(data=result)
        else:
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def delete(self, request):
        """
        删除机房
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 删除机房
        Cabinet.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)

