import shutil

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import CxfbForm
from api.models import Cxfb
from api.serializers import CxfbSerializer
from api.utils.auth_util import check_login


class CxfbView(APIView):

    def get(self, request):
        """
        获取所有
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            pl_data = CxfbSerializer(instance=Cxfb.objects.all(), many=True)

            result['data'] = pl_data.data
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

        new_obj = CxfbForm(request.data)
        if new_obj.is_valid():
            new_obj = new_obj.save()
            result['data'] = CxfbSerializer(instance=new_obj, many=False).data
            return Response(data=result)
        else:
            print(new_obj.errors)
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    #
    # def put(self, request):
    #     """
    #     修改pl
    #     """
    #     result = {"code": "1000", 'data': '', 'error': ""}
    #     try:
    #
    #         # 修改pl
    #         pl_from_db = ProductLine.objects.filter(pk=request.data.get('id')).first()
    #         edit_pl = ProductLineForm(request.data, instance=pl_from_db)
    #         if edit_pl.is_valid():
    #             edited_pl = edit_pl.save()
    #             result['data'] = ProductLineModelSerializer(instance=edited_pl, many=False).data
    #             return Response(data=result)
    #         else:
    #             result['code'] = 1001
    #             request['error'] = 'field not valid!'
    #             return Response(data=result)
    #     except Exception as e:
    #         result['code'] = '1001'
    #         result['error'] = 'some unknown error!'
    #         return Response(data=result)

    def delete(self, request):
        """
        删除
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            print(request.query_params.get("id"))
            # 删除
            d_id = request.query_params.get("id")
            if clean_cxfb_common(d_id):
                Cxfb.objects.filter(pk=d_id).delete()
                return Response(data=result)
            else:
                result['code'] = '1001'
                return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)


@api_view(('GET',))
def clean_cxfb(request):
    """
    clean cxfb
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

        d_id = request.query_params.get('id')
        result = clean_cxfb_common(d_id)
        if result:
            return Response(data=result)
        else:
            result['code'] = '1001'
            return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


def clean_cxfb_common(d_id):
    try:
        cxfb = Cxfb.objects.filter(pk=d_id).first()
        deploy_path = cxfb.project.deploy_path
        cxfb.status = '未部署'
        cxfb.save()
        shutil.rmtree(deploy_path)  # 递归删除文件夹
        return True
    except Exception:
        return False
