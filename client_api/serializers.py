from rest_framework import serializers

from client_api.models import Client


class ClientSerializer(serializers.Serializer):
    ip = serializers.CharField()
    host_name = serializers.CharField()
    cpu_model = serializers.CharField()
    cpu_num = serializers.CharField()
    memory = serializers.CharField()
    disk = serializers.CharField()
    system = serializers.CharField()
    cabinet = serializers.SerializerMethodField()

    def get_cabinet(self, obj):
        if obj.cabinet:
            return obj.cabinet.name
        else:
            return ""