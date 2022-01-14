from django.urls import path
from restaurant_management import views

urlpatterns = [
    path("signin", views.signin, name="signin"),
    path("signout/", views.signout, name="signout"),
    path("", views.home, name="home"),
    path("take_away/", views.takeAway, name="take_away"),
    path("cal_events/", views.EventsView.as_view(), name="cal_events"),
    path("vip_member/", views.vipMember, name="vip_member"),
    path("statistics/", views.statistics, name="statistics"),
    path("setting/", views.setting, name="setting"),
    path("booking/", views.booking, name = "booking")
]
