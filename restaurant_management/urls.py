from django.urls import path
from restaurant_management import views

urlpatterns = [
    path("", views.home, name="home"),    
    path("hoadon/<int:ma_hoa_don>/", views.hoadon, name = "hoadon"),
    path("take_away/", views.takeAway, name="take_away"),
    path("events/", views.events, name="events"),
    path("vip_member/", views.vipMember, name="vip_member"),
    path("statistics/", views.statistics, name="statistics"),
    path("setting/", views.setting, name="setting"),
    path("login", views.signin, name = "signin"),
]