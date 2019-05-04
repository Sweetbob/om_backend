from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import CollectiveForm
from api.models import Collective
from api.serializers import CollectiveModelSerializer
from api.utils.auth_util import check_login


class CollectiveView(APIView):

    def get(self, request):
        """
        获取所有collective
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        collectives = Collective.objects.all()
        collectives_data = CollectiveModelSerializer(instance=collectives, many=True)
        print(collectives_data.data)

        result['data'] = collectives_data.data
        return Response(data=result)

    def post(self, request):
        """
        添加collecitve
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        new_collecitve = CollectiveForm(request.data)
        print(request.data)
        if new_collecitve.is_valid():
            cabinet = new_collecitve.save()
            result['data'] = CollectiveModelSerializer(instance=cabinet, many=False).data
            return Response(data=result)
        else:
            print(new_collecitve.errors)
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def put(self, request):
        """
        修改机柜
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        # 修改
        collective_from_db = Collective.objects.filter(pk=request.data.get('id')).first()
        edit_c = CollectiveForm(request.data, instance=collective_from_db)
        if edit_c.is_valid():
            edited_c = edit_c.save()
            result['data'] = CollectiveModelSerializer(instance=edited_c, many=False).data
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
        Collective.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)

