from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import ProjectForm
from api.models import Project
from api.serializers import ProjectModelSerializer
from api.utils.auth_util import check_login


class ProjectView(APIView):

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

        ps = Project.objects.all()
        ps_data = ProjectModelSerializer(instance=ps, many=True)
        print(ps_data.data)

        result['data'] = ps_data.data
        return Response(data=result)

    def post(self, request):
        """
        add project
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        new_project = ProjectForm(request.data)
        print(request.data)
        if new_project.is_valid():
            project = new_project.save()
            result['data'] = ProjectModelSerializer(instance=project, many=False).data
            return Response(data=result)
        else:
            print(new_project.errors)
            result['code'] = 1001
            result['error'] = 'field not valid!'
            return Response(data=result)

    def put(self, request):
        """
        modify project
        """
        result = {"code": "1000", 'data': '', 'error': ""}

        # 修改
        p_from_db = Project.objects.filter(pk=request.data.get('id')).first()
        edit_p = ProjectForm(request.data, instance=p_from_db)
        if edit_p.is_valid():
            edit_p = edit_p.save()
            result['data'] = ProjectModelSerializer(instance=edit_p, many=False).data
            return Response(data=result)
        else:
            print(edit_p.errors)
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
        Project.objects.filter(pk=request.query_params.get("id")).delete()
        return Response(data=result)

