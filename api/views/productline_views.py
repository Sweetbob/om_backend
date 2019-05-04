from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import ProductLineForm
from api.models import ProductLine
from api.serializers import ProductLineModelSerializer


class ProductLineView(APIView):

    def get(self, request):
        """
        获取所有
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            # 返回人员数据
            pl_data = ProductLineModelSerializer(instance=ProductLine.objects.all(), many=True)

            result['data'] = pl_data.data
            return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def post(self, request):
        """
        添加productline
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        # 添加productline
        new_obj = ProductLineForm(request.data)
        if new_obj.is_valid():
            new_obj = new_obj.save()
            result['data'] = ProductLineModelSerializer(instance=new_obj, many=False).data
            return Response(data=result)
        else:
            result['code'] = 1001
            request['error'] = 'field not valid!'
            return Response(data=result)


    def put(self, request):
        """
        修改pl
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            # 修改pl
            pl_from_db = ProductLine.objects.filter(pk=request.data.get('id')).first()
            edit_pl = ProductLineForm(request.data, instance=pl_from_db)
            if edit_pl.is_valid():
                edited_pl = edit_pl.save()
                result['data'] = ProductLineModelSerializer(instance=edited_pl, many=False).data
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

            print(request.query_params.get("id"))
            # 删除运维人员
            ProductLine.objects.filter(pk=request.query_params.get("id")).delete()
            return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)
