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
    # hoa_don = None
    # if (request.method == 'POST'):
    #     if "chon_ban" in request.POST :
    #         so_ban = request.POST.get(so_ban)
    #         print(so_ban)
    #         ban = Ban.objects.get(so_ban = so_ban)
    #         ma_hoa_don = ban.get_mahoadon()
    #         if (ma_hoa_don != None):
    #             hoa_don = HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
    #     if "add_hoa_don" in request.POST :
    #         a =0
              
    return render(request, "management/home.html", 
                  {
                        'bans' : bans,
                        # 'hoa_don': hoa_don
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