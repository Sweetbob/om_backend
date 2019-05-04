from rest_framework import serializers
from api.models import Cabinet, Charger, SiteNavi, Collective, ProductLine, Project, AuthCenter, Interval, Crontab


class ChargerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charger
        fields = "__all__"


class AuthCenterModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthCenter
        fields = "__all__"


class IntervalModelSerializer(serializers.Serializer):
    id = serializers.CharField()
    interval_amount = serializers.IntegerField()
    interval_measure = serializers.CharField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.interval_amount) + "/" + obj.interval_measure


class MissionSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    type = serializers.CharField()
    content = serializers.CharField()
    # interval = serializers.SerializerMethodField()
    enabled = serializers.CharField()
    type = serializers.CharField()
    description = serializers.CharField()
    crontab = serializers.SerializerMethodField()
    c_id = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    # def get_interval(self, obj):
    #     if obj.interval:
    #         return str(obj.interval.interval_amount) + "/" + obj.interval.interval_measure
    #     else:
    #         return ''

    def get_crontab(self, obj):
        if obj.crontab:
            return str(obj.crontab.minute) + " " + obj.crontab.hour + " " +obj.crontab.day_week + " " \
                   +obj.crontab.day_month + " " +obj.crontab.month_year
        else:
            return ''
    def get_c_id(self, obj):
        if obj.crontab:
            return obj.crontab.id
        else:
            return ''

    def get_status(self, obj):
        if obj.enabled == '1':
            return 'running'
        else:
            return 'stopped'


class CrontabModelSerializer(serializers.Serializer):

    id = serializers.CharField()
    minute = serializers.CharField()
    hour = serializers.CharField()
    day_week = serializers.CharField()
    day_month = serializers.CharField()
    month_year = serializers.CharField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        return str(obj.minute) + " " + obj.hour + " " +obj.day_week + " " +obj.day_month + " " +obj.month_year


class ProjectModelSerializer(serializers.Serializer):
    id = serializers.CharField()
    p_name = serializers.CharField()
    p_desc = serializers.CharField()
    language_type = serializers.CharField()
    project_type = serializers.CharField()
    server_type = serializers.CharField()
    app_frame = serializers.CharField()
    warehouse_type = serializers.CharField()
    warehouse_url = serializers.CharField()
    deploy_path = serializers.CharField()
    conf_path = serializers.CharField()
    productline = serializers.SerializerMethodField()
    charger = serializers.SerializerMethodField()
    productline_name = serializers.SerializerMethodField()
    c_name = serializers.SerializerMethodField()
    c_tel = serializers.SerializerMethodField()

    def get_productline_name(self, obj):
        if obj.productline:
            return obj.productline.name
        else:
            return ""
    def get_productline(self, obj):
        if obj.productline:
            return obj.productline.id
        else:
            return ""
    def get_charger(self, obj):
        if obj.charger:
            return obj.charger.id
        else:
            return ""

    def get_c_name(self, obj):
        if obj.charger:
            return obj.charger.name
        else:
            return ""
    def get_c_tel(self, obj):
        if obj.charger:
            return obj.charger.tel
        else:
            return ""


class ProductLineModelSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    desc = serializers.CharField()
    c_id = serializers.SerializerMethodField()
    c_name = serializers.SerializerMethodField()
    c_tel = serializers.SerializerMethodField()
    c_email = serializers.SerializerMethodField()

    def get_c_id(self, obj):
        return obj.charger.id

    def get_c_name(self, obj):
        return obj.charger.name

    def get_c_tel(self, obj):
        return obj.charger.tel

    def get_c_email(self, obj):
        return obj.charger.email


class SiteNaviModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteNavi
        fields = "__all__"


class CollectiveModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collective
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