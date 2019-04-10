
from django.urls import path
from api.views import login_views

urlpatterns = [
    path('login/', login_views.LoginView.as_view()),
]
