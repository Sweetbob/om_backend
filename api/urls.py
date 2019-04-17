
from django.urls import path
from api.views import login_views, cabinet_views, client_views, charger_views, room_views

urlpatterns = [
    path('login/', login_views.LoginView.as_view()),

    path('client/', client_views.ClientStaticView.as_view()),

    path('cabinet/', cabinet_views.CabinetView.as_view()),

    path('charger/', charger_views.ChargerView.as_view()),

    path('room/', room_views.RoomView.as_view()),

    path('client_num/', client_views.client_extra_num),

    path('client_detail/', client_views.client_detail),

    # path('ping/', client_views.ping),


]
