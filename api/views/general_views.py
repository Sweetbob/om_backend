from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.models import SiteNavi
from api.serializers import SiteNaviModelSerializer


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