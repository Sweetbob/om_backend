from rest_framework.response import Response
from rest_framework.views import APIView

from api.forms import RoomForm
from api.models import Room
from api.serializers import RoomSerializer
from api.utils.auth_util import check_login
from client_api.models import Client


class RoomView(APIView):

    def get(self, request):
        """
        获取所有机房
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 返回机房数据
        rooms = Room.objects.all()
        for r in rooms:
            # 计算每个机房的主机数
            r.machine_num = Client.objects.filter(cabinet__room=r.pk).count()
            r.save()
        room_data = RoomSerializer(instance=rooms, many=True)
        print(room_data.data)

        result['data'] = room_data.data
        return Response(data=result)
        # except Exception as e:
        #     result['code'] = '1001'
        #     result['error'] = 'some unknown error!'
        #     return Response(data=result)

    def post(self, request):
        """
        添加机房
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 添加机房
            new_room = RoomForm(request.data)
            print(request.data)
            if new_room.is_valid():
                room = new_room.save()
                result['data'] = RoomSerializer(instance=room, many=False).data
                return Response(data=result)
            else:
                print(new_room.errors)
                result['code'] = 1001
                result['error'] = 'field not valid!'
                return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)

    def put(self, request):
        """
        修改机房
        """
        result = {"code": "1000", 'data': '', 'error': ""}
        # try:
        # 验证登陆情况
        if not check_login(token=request.query_params.get('token')):
            result['code'] = "1001"
            result['error'] = 'not valid token!'
            return Response(data=result)

        # 修改机房
        room_from_db = Room.objects.filter(pk=request.data.get('id')).first()
        edit_room = RoomForm(request.data, instance=room_from_db)
        if edit_room.is_valid():
            edited_room = edit_room.save()
            result['data'] = RoomSerializer(instance=edited_room, many=False).data
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
        try:
            # 验证登陆情况
            if not check_login(token=request.query_params.get('token')):
                result['code'] = "1001"
                result['error'] = 'not valid token!'
                return Response(data=result)

            # 删除机房
            Room.objects.filter(pk=request.query_params.get("id")).delete()
            return Response(data=result)
        except Exception as e:
            result['code'] = '1001'
            result['error'] = 'some unknown error!'
            return Response(data=result)
