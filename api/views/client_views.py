from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.utils.auth_util import check_login
from api.utils.network_util import is_alive
from client_api.forms import ClientForm
from client_api.models import Client
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
            if is_alive(item.get("ip")):
                item['status'] = '运行中...'
            else:
                item['status'] = '非运行状态'
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


# @api_view(('GET',))
# def ping(request):
#     """
#     ping 主机
#     """
#     ip = request.query_params.get("ip")
#     result = {"code": "1000"}
#     nm = nmap.PortScanner()
#     nm.scan(hosts=ip, arguments='-sn')
#     # 返回主机数
#     client_num = Client.objects.all().count()
#     result['data'] = {"num": client_num}
#     return Response(data=result)

