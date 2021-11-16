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
    ma_hoa_don = None
    bans = Ban.objects.all()
    menu = Menu.objects.all()
    mon_an = MonAn.objects.all()
    
    try :
        hoa_don = HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        dat_mon = DatMon.objects.filter(ma_hoa_don = ma_hoa_don)
        return render(request, "management/home.html", 
                {
                    'bans' : bans,
                    'mon_an':mon_an,
                    'menu': menu,
                    'hoa_don':hoa_don,
                    'ma_hoa_don': ma_hoa_don,
                    'dat_mon': dat_mon,
                })
    except:
            
        return render(request, "management/home.html", 
                    {
                            'bans' : bans,
                            'menu' : menu,
                            'mon_an':mon_an,
                            'ma_hoa_don': ma_hoa_don,
                    })
    
def home1(request):
    bans = Ban.objects.all()
    context = {
        'bans': bans
    }
    if "choose_ban" in request.POST :
        so_ban = request.POST.get("choose_ban")
        print(so_ban)
        
        # try:
        #     hoadon = HoaDon.objects.get(ma)
    return render(request, "management/home1.html", context)    
    
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