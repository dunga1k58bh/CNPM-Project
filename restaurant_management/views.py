from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from restaurant_management import models
from restaurant_management.models import *
# Create your views here.


def signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        if username and password :
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else :
                messages.error(request, "Nhập sai tên đăng nhập hoặc mật khẩu")    
        else :
            messages.error(request, 'Nhập thiếu tên đăng nhập hoặc mật khẩu')
    
    return render(request, "authentication/signin.html", {})
   

def home(request):
    bans = Ban.objects.all()     
    return render(request, "management/home.html", 
                  {
                        'bans' : bans,
                  })
    
def hoadon(request , ma_hoa_don):
    bans = Ban.objects.all()
    hoadons = HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
    return render(request, "management/hoadon.html",
                  {
                      'bans' : bans,
                      'hoadons':hoadon
                  })
    
def takeAway(request):
    return render(request, "management/take_away.html")

def events(request):
    return render(request, "management/events.html")

def vipMember(request):
    return render(request, "management/vip_member.html")


def statistics(request):
    return render(request, "management/statistics.html")


def setting(request):
    return render(request, "management/setting.html")