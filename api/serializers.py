from rest_framework import serializers

from api.models import Cabinet, Charger




class ChargerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = "__all__"


class RoomSerializer(serializers.Serializer):

    id = serializers.CharField()
    no = serializers.CharField()
    name = serializers.CharField()
    address = serializers.CharField()
    machine_num = serializers.IntegerField()
    charger = serializers.SerializerMethodField()

    def get_charger(self, obj):
        return obj.charger.name


class CabinetSerializer(serializers.Serializer):

    id = serializers.CharField()
    no = serializers.CharField()
    name = serializers.CharField()
    address = serializers.CharField()
    machine_num = serializers.IntegerField()
    charger = serializers.SerializerMethodField()
    room = serializers.SerializerMethodField()

    def get_room(self, obj):
        return obj.room.name

    def get_charger(self, obj):
        return obj.room.charger.name