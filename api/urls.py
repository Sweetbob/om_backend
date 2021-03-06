
from django.urls import path
from api.views import login_views, cabinet_views, client_views, charger_views, room_views, general_views, \
    collective_views, productline_views, project_view, authcenter_views, interval_view, crontab_view, mission_view, \
    cxfb_view

urlpatterns = [
    path('login/', login_views.LoginView.as_view()),

    path('client/', client_views.ClientStaticView.as_view()),

    path('cabinet/', cabinet_views.CabinetView.as_view()),
    path('cabinet_of_room/', cabinet_views.cabinet_of_room),
    path('client_of_cabinet/', client_views.client_of_cabinet),

    path('firewall_status/', client_views.firewall_status),
    path('host_name_changing/', client_views.host_name_changing),
    path('firewall_changing/', client_views.firewall_changing),


    path('collective/', collective_views.CollectiveView.as_view()),

    path('authcenter/', authcenter_views.AuthCenterView.as_view()),
    path('do_auth/', authcenter_views.auth_extra_doauth),
    path('project/', project_view.ProjectView.as_view()),

    path('interval/', interval_view.IntervalView.as_view()),
    path('crontab/', crontab_view.CrontabView.as_view()),
    path('mission/', mission_view.MissionView.as_view()),
    path('start_mission/', mission_view.start_mission),
    path('stop_mission/', mission_view.stop_mission),
    path('mission_log/', mission_view.mission_log),
    path('ansible_log/', mission_view.ansible_log),
    path('shell_log/', mission_view.shell_log),
    path('execute_shell/', mission_view.execute_shell),
    path('execute_playbook/', mission_view.execute_playbook),
    path('execute_ansible_command/', mission_view.execute_ansible_command),
    path('get_playbook/', mission_view.get_playbook),
    path('cxfb/', cxfb_view.CxfbView.as_view()),
    path('clean_cxfb/', cxfb_view.clean_cxfb),
    path('deploy/', cxfb_view.deploy),
    path('deploy_log/', cxfb_view.deploy_log),


    path('current_realtime_info/', client_views.current_realtime_info),
    path('realtime_infos/', client_views.realtime_infos),


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

    path('mysql_info/', general_views.mysql_info),
    path('set_mysql_info/', general_views.set_mysql_info),

    path('sitenavis/', general_views.sitenavis),

    path('reboot/', client_views.client_reboot),

    path('ping/', client_views.ping),
    path('machine_num_by_type/', client_views.machine_num_by_type),


]
