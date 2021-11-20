from datetime import time
from django.core.checks import messages
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
import datetime
from django.utils.tree import Node
import pytz
from restaurant_management import models
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
    bans = models.Ban.objects.all()
    menu = models.Menu.objects.all()
    mon_ans = models.MonAn.objects.all()
    context = {
        'bans': bans,
        'menu': menu,
        'mon_ans': mon_ans,
    }
    if "choose_ban" in request.POST :
        so_ban = request.POST.get("choose_ban")
        context.update({
                    'so_ban':so_ban
                    })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon = ban.ma_hoa_don
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            if hoadon is not None:
                context.update({
                    'hoadon' : hoadon,
                    'dat_mons': dat_mons
                    })
                ban.trang_thai ="đang sử dụng"
                ban.save()
        except:
            print("ban nay chua co hoa don")
            ban.trang_thai ="rảnh"
            ban.save()
    if "add_hoa_don" in request.POST :
        # Đoạn này để tạo hóa đơn và thêm hóa đơn vào bàn
        so_ban = request.POST.get("add_hoa_don")
        date = timezone.localtime(timezone.now())
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)

        # Lấy ra danh sách mã món đã thêm và số lượng để add vào bảng Đặt món
        
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        # Tính tiền đặt món mới
        giahoadon =0        
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)
            
        # Kiểm tra: Nếu bàn có hóa đơn thì cộng tiền vào đơn giá của hóa đơn đó
        # không thì tọa hóa đơn mới
        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon=ban.ma_hoa_don
        if hoadon is not None:
            hoadon.don_gia = hoadon.don_gia +giahoadon        
        else  :   
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = giahoadon, phuong_thuc_thanh_toan ="tien_mat", so_ban= so_ban, ma_nhan_vien = nhanvien)
            ban.ma_hoa_don= hoadon
        ban.trang_thai ="đang sử dụng"
        ban.save()
        hoadon.save()
        #Lưu món đặt mới vào csdl
        ma_hoa_don = hoadon.ma_hoa_don
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            dat_mon = models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)
    
    if "remove_hoa_don" in request.POST :
        so_ban = request.POST.get("remove_hoa_don")
        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon = ban.ma_hoa_don
        if hoadon is not None:
            ma_hoa_don = hoadon.ma_hoa_don
            models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don).delete()
            ban.ma_hoa_don = None
            ban.trang_thai="rảnh"
            ban.save()
            hoadon.delete()

    #Khi click thanh toán thì xóa hóa đơn khỏi bàn trả về bàn chưa có hóa đơn     
    if "pay" in request.POST :
        so_ban = request.POST.get("pay")
        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon = ban.ma_hoa_don
        if hoadon is not None:
            ma_hoa_don = hoadon.ma_hoa_don
            ban.ma_hoa_don = None
            ban.trang_thai= "rảnh"
            ban.save()
    return render(request, "management/home.html", context)
    


    
def takeAway(request):
    menu = models.Menu.objects.all()
    mon_ans = models.MonAn.objects.all()
    so_ban = 8
    context = {
        'menu': menu,
        'mon_ans': mon_ans,
    }
    # Tương ứng bên giao diện là thanh toán, khi click thì tạo hóa đơn và lưu, mặc định số bàn là 8
    if "add_hoa_don" in request.POST :
        date = timezone.localtime(timezone.now())
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)
        giahoadon =0        
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)


        hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = giahoadon, phuong_thuc_thanh_toan ="tien_mat", so_ban= so_ban, ma_nhan_vien = nhanvien)
        hoadon.save()
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            dat_mon = models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)

    return render(request, "management/take_away.html", context)

def events(request):
    return render(request, "management/events.html")

def vipMember(request):
    return render(request, "management/vip_member.html")


def statistics(request):
    return render(request, "management/statistics.html")


def setting(request):
    return render(request, "management/setting.html")