from django.urls import path
from restaurant_management import views

urlpatterns = [
    
    path("", views.home, name="home"), 
    path("home1", views.home1, name= "home1"),   
    path("", views.home, name="home"),    
    path("take_away/", views.takeAway, name="take_away"),
    path("events/", views.events, name="events"),
    path("vip_member/", views.vipMember, name="vip_member"),
    path("statistics/", views.statistics, name="statistics"),
    path("setting/", views.setting, name="setting"),
    path("login", views.signin, name = "signin"),
]