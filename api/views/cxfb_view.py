import datetime
import os
import shutil
import time

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


    def put(self, request):
        """
        修改
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            # 修改
            c_from_db = Cxfb.objects.filter(pk=request.data.get('id')).first()
            edit_c = CxfbForm(request.data, instance=c_from_db)
            if edit_c.is_valid():
                edited_c = edit_c.save()
                result['data'] = CxfbSerializer(instance=edited_c, many=False).data
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
        删除
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:

            print(request.query_params.get("id"))
            # 删除
            d_id = request.query_params.get("id")
            r = clean_cxfb_common(d_id)
            print(r)
            if r:
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
        r = clean_cxfb_common(d_id)
        if r:
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
        if os.path.exists(deploy_path):
            shutil.rmtree(deploy_path)  # 递归删除文件夹

        return True
    except Exception:
        return False


@api_view(('GET',))
def deploy(request):
    """
    deploy cxfb
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
        cxfb = Cxfb.objects.get(pk=d_id)
        project = cxfb.project
        warehouse_type = project.warehouse_type
        log_file = "/opt/log/deploy_"+ project.p_name + "_log.log"
        os.system("echo '开始部署.....\n' > " + log_file)
        os.system("echo -e '项目名:" + project.p_name + "\n' >> " + log_file + "\n")
        if warehouse_type == '2' or warehouse_type == 2:
            deploy_path = project.deploy_path
            temp_path = "/opt/cxfb/temp/"
            if cxfb.if_clean:
                if os.path.exists(temp_path):
                    shutil.rmtree(temp_path)  # 递归删除文件夹
            warehouse_url = project.warehouse_url
            git_command = "mkdir -p " + temp_path + ";cd "+temp_path+";git clone " + warehouse_url + " >> " + log_file
            os.system("echo -e '开始从git仓库下载项目.....\n' >> " + log_file)
            os.system(git_command)
            os.system("echo -e '开始分发.....\n' >> " + log_file)
            for c in cxfb.machines.all():
                print('ssh root@' + c.ip + ' "rm -rf ' + deploy_path + '"')
                os.system('ssh root@' + c.ip + ' "rm -rf ' + deploy_path + '"')
                print('ssh root@' + c.ip + ' "mkdir  -p ' + deploy_path + '"')
                os.system('ssh root@' + c.ip + ' "mkdir  -p ' + deploy_path + '"')
                print('scp -r ' + temp_path + ' root@' + c.ip + ':' + deploy_path)
                os.system('scp -r ' + temp_path + ' root@' + c.ip + ':' + deploy_path)
            os.system("echo -e '分发完成。 开始执行命令.........\n' >> " + log_file)
            shell = cxfb.shell
            if not shell:
                os.system("echo -e '无部署命令执行\n' >> " + log_file)
            cxfb.status = "已部署"
            cxfb.save()
            os.system("echo -e '部署完成 ' >> " + log_file)
        else:
            print("no")
        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)


@api_view(('GET',))
def deploy_log(request):
    """
    get deploy log
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

        id = request.query_params.get('id')
        cxfb = Cxfb.objects.filter(pk=id).first()
        c_name = cxfb.project.p_name
        updated_time = ''
        log = ""
        file_name = "/opt/log/deploy_" + c_name + "_log.log"
        try:

            with open(file_name) as log_file:
                log = log_file.read()
            updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.stat(file_name).st_ctime))
            print(updated_time)
        except Exception:
            print('error')
        result['data'] = {
            "log": log,
            "updated_time": updated_time,
            'c_name': c_name
        }

        return Response(data=result)
    except Exception as e:
        result['code'] = '1001'
        result['error'] = 'some unknown error!'
        return Response(data=result)