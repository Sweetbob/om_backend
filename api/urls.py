
from django.urls import path
from api.views import login_views, cabinet_views, client_views, charger_views, room_views, general_views, \
    collective_views, productline_views, project_view, authcenter_views, interval_view, crontab_view, mission_view

urlpatterns = [
    path('login/', login_views.LoginView.as_view()),

    path('client/', client_views.ClientStaticView.as_view()),

    path('cabinet/', cabinet_views.CabinetView.as_view()),
    path('collective/', collective_views.CollectiveView.as_view()),

    path('authcenter/', authcenter_views.AuthCenterView.as_view()),
    path('do_auth/', authcenter_views.auth_extra_doauth),
    path('project/', project_view.ProjectView.as_view()),

    path('interval/', interval_view.IntervalView.as_view()),
    path('crontab/', crontab_view.CrontabView.as_view()),
    path('mission/', mission_view.MissionView.as_view()),
    path('start_mission/', mission_view.start_mission),


    path('charger/', charger_views.ChargerView.as_view()),

    path('productline/', productline_views.ProductLineView.as_view()),

    path('room/', room_views.RoomView.as_view()),

    path('client_num/', client_views.client_extra_num),
    path('room_num/', client_views.room_extra_num),
    path('cabinet_num/', client_views.cabinet_extra_num),


    path('client_detail/', client_views.client_detail),

    path('poweroff/', client_views.client_poweroff),

    path('change_pw/', client_views.change_pw),

    path('add_sitenavi/', general_views.add_sitenavi),

    path('sitenavis/', general_views.sitenavis),

    path('reboot/', client_views.client_reboot),

    path('ping/', client_views.ping),


]
