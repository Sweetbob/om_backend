from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import AuthCenterForm
from api.models import AuthCenter
from api.serializers import AuthCenterModelSerializer
from api.utils.auth_util import check_login, SshCopy


class AuthCenterView(APIView):

    def get(self, request):
        """
        获取所有
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        acs = AuthCenter.objects.all()
        ac_data = AuthCenterModelSerializer(instance=acs, many=True)
        print(ac_data.data)

        result['data'] = ac_data.data
        return Response(data=result)

    def post(self, request):
        """
        添加auth
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        new_ac = AuthCenterForm(request.data)
        print(request.data)
        if new_ac.is_valid():
            ac = new_ac.save()
            result['data'] = AuthCenterModelSerializer(instance=ac, many=False).data
            return Response(data=result)
        else:
            print(new_ac.errors)
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
        AuthCenter.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)


@api_view(('POST',))
def auth_extra_doauth(request):
    """
    authenticate
    """
    result = {"code": "1000"}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)
    user = request.data.get('ssh')
    host = request.data.get('host')
    password = request.data.get('password')
    port = request.data.get('port')
    ssh_copy = SshCopy(user=user, host=host, passwd=password, port=port)
    excu_result = ssh_copy.send()
    print('ssssss',excu_result)
    if excu_result == 'not':
        result['code'] = '1001'

    print(result)
    return Response(data=result)





