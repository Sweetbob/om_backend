from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import SiteNavi
from api.serializers import SiteNaviModelSerializer
from api.utils.auth_util import check_login
from om_backend.settings import conf, write_conf


@api_view(('POST',))
def add_sitenavi(request):
    result = {"code": "1000", 'data': '', 'error': ""}
    site_name = request.data.get("site_name")
    site_address = request.data.get("site_address")
    desc = request.data.get("desc")
    SiteNavi(site_name=site_name, site_address=site_address, desc=desc).save()
    return Response(data=result)


@api_view(('GET',))
def sitenavis(request):
    result = {"code": "1000", 'data': '', 'error': ""}
    sitenavis = SiteNavi.objects.all()
    data = SiteNaviModelSerializer(instance=sitenavis, many=True)
    result['data'] = data.data
    return Response(data=result)


@api_view(('GET',))
def mysql_info(request):
    result = {"code": "1000", 'data': '', 'error': ""}
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)

    mysql_ip = conf.get('global', "HOST")
    mysql_port = conf.get('global', "PORT")
    mysql_name = conf.get('global', "NAME")
    mysql_user = conf.get('global', "USER")
    mysql_password = conf.get('global', "PASSWORD")
    result['data'] = {
        "mysql_ip": mysql_ip,
        "mysql_port": mysql_port,
        "mysql_name": mysql_name,
        "mysql_user": mysql_user,
        "mysql_password": mysql_password,
    }
    return Response(data=result)


@api_view(('POST',))
def set_mysql_info(request):
    result = {"code": "1000", 'data': '', 'error': ""}
    # try:
    # 验证登陆情况
    if not check_login(token=request.query_params.get('token')):
        result = {
            "code": "1001",
            'error': 'not valid token!'
        }
        return Response(data=result)

    conf.set('global', "HOST", request.data.get('mysql_ip'))
    conf.set('global', "PORT", request.data.get('mysql_port'))
    conf.set('global', "NAME", request.data.get('mysql_name'))
    conf.set('global', "USER", request.data.get('mysql_user'))
    conf.set('global', "PASSWORD", request.data.get('mysql_password'))
    write_conf()
    return Response(data=result)
    # except Exception as e:
    #     print(e)
    #     result['code'] = '1001'
    #     result['error'] = 'some unknown error!'
    #     return Response(data=result)
