import uuid

from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User


class LoginView(APIView):

    def post(self, request):
        result = {"code": "1000"}

        # authenticate user and password
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username, password=password)
        if not user:
            result['code'] = '1001'
            result['message'] = 'User not exist or Password incorrect!'
            return Response(result)

        # generate token
        token = uuid.uuid4()
        user.update(token=token)
        result['token'] = token
        return Response(data=result)
