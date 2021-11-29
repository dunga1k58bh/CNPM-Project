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
import json
from django.db.models import Sum
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

        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon=ban.ma_hoa_don
        if hoadon is None:  
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = 0, phuong_thuc_thanh_toan ="tien_mat", so_ban= so_ban, ma_nhan_vien = nhanvien)
            ban.ma_hoa_don= hoadon
        ban.trang_thai ="đang sử dụng"
        ban.save()
        #Lưu món đặt mới vào csdl
        giahoadon =0 
        ma_hoa_don = hoadon.ma_hoa_don
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            #
            mdds = models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don )
            print(mdds)
            i =0
            mmm =0
            #
            if so_luong != '0' :
                #
                for mdd in mdds:
                    if ma_mon == mdd.ma_mon.ma_mon :
                        new_so_luong = int(so_luong) + int(mdd.so_luong)
                        mdd.delete()
                        models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = new_so_luong)
                        mmm= ma_mon
                        i=1
                #
                if i==0 :
                    dat_mon = models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)
                else :
                    for mdd in mdds:
                        if mmm != mdd.ma_mon.ma_mon:
                            models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon = mdd.ma_mon, so_luong = mdd.so_luong)
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)
        hoadon.don_gia= hoadon.don_gia + giahoadon
        hoadon.save()
        
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

def booking (request):
    bans = models.Ban.objects.all()
    context = {
        'bans': bans,
    }
    if "choose_ban" in request.POST :
        so_ban = request.POST.get("choose_ban")
        context.update({
                    'so_ban':so_ban
                    })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            print(so_ban)
            print(ban)
            dat_ban = models.DatMon.objects.filter(so_ban = ban)
            if dat_ban is not None:
                context.update({
                    'dat_ban': dat_ban
                    })
                ban.trang_thai ="đang đợi"
                ban.save()
        except:
            print("ban nay chua co khach dat")
            ban.save()
    if "booking_table" in request.POST :
        so_ban = request.POST.get("booking_table")
        ban = models.Ban.objects.get(so_ban = so_ban)
        ho_ten = request.POST.get("ho_ten")
        sdt = request.POST.get("sdt")
        date = timezone.localtime(timezone.now())
        dat_ban= models.DatBan.objects.create(ho_ten = ho_ten, sdt = sdt, so_ban = ban, thoi_gian = date)
        ban.trang_thai = "đang đợi"
        ban.save()
        context.update({
            'dat_ban': dat_ban
        })
    if "remove_booking_table" in request.POST :
        so_ban = request.POST.get("remove_booking_table")
        ban = models.Ban.objects.get(so_ban = so_ban)
        dat_ban = models.DatBan.objects.filter(so_ban = so_ban)
        dat_ban.delete()
        ban.trang_thai = "rảnh"
        ban.save()
        context.update({
            'dat_ban': dat_ban
        })
    return render(request, "management/booking.html", context)

def takeAway(request):
    menu = models.Menu.objects.all()
    mon_ans = models.MonAn.objects.all()
    context = {
        'menu': menu,
        'mon_ans': mon_ans,
    }
    # Tương ứng bên giao diện là lưu hóa đơn, khi click thì tạo hóa đơn và lưu, mặc định số bàn là 8
    if "add_hoa_don" in request.POST :    
        ma_hoa_don = request.POST.get("add_hoa_don")
        date = timezone.localtime(timezone.now())
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)
        giahoadon =0  
        
        if ma_hoa_don != '':  
            hoadon = models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        else:          
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = giahoadon, phuong_thuc_thanh_toan ="tien_mat",so_ban= 8,  ma_nhan_vien = nhanvien)  
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            if so_luong != '0':
                dat_mon = models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)

        hoadon.don_gia = hoadon.don_gia + giahoadon
        hoadon.save()
        dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        context.update({
            'mahoadon' : hoadon.ma_hoa_don ,
            'tongtien' : hoadon.don_gia,
            'dat_mons': dat_mons ,
        })

    # Xóa hóa đơn
    if "remove_hoa_don" in request.POST :
        ma_hoa_don= request.POST.get("remove_hoa_don")
        hoadon= models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        if hoadon is not None:
            models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don).delete()
            hoadon.delete()
            context.update({
                'ma_hoa_don': ''
            })
    # Thanh toán hóa đơn
    if "pay" in request.POST:
        ma_hoa_don= request.POST.get("pay")
        hoadon= models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        if hoadon is not None:
            context.update({
                'ma_hoa_don': ''
            })

    return render(request, "management/take_away.html", context)

def events(request):
    return render(request, "management/events.html")

def vipMember(request):
    menus = models.Menu.objects.all()
    khachhangs = models.KhachHang.objects.all()
    thethanhviens = models.TheThanhVien.objects.all()
    return render(request, "management/vip_member.html",
                {
                    'menu' : menus,
                    'thethanhviens' : thethanhviens,
                    'khachhangs' : khachhangs
                })


def statistics(request):
    ma_mons = []
    so_luongs = []
    ma_hoa_dons = []
    ten_mons = []

    dat_mons = models.DatMon.objects.values('ma_mon').annotate(Sum('so_luong'))
    for dat_mon in dat_mons:
        ma_mons.append(dat_mon['ma_mon'])
        so_luongs.append(dat_mon['so_luong__sum'])
        mon_an = models.MonAn.objects.get(ma_mon=dat_mon['ma_mon'])
        ten_mons.append(mon_an.ten_mon)

    context = {
        'ma_mons': json.dumps(ma_mons),
        'so_luongs': json.dumps(so_luongs),
        'ten_mons': json.dumps(ten_mons),
    }
    print(context)

    return render(request, "management/statistics.html", context)


def setting(request):
    menus = models.Menu.objects.all()
    monans = models.MonAn.objects.all() 
    bans = models.Ban.objects.all() 
    nhanviens = models.NhanVien.objects.all() 
    soluong_ban = models.Ban.objects.filter().count()   
    return render(request, "management/setting.html", 
                  {
                        'menus' : menus,
                        'monans' : monans,
                        'bans' : bans,
                        'nhanviens' : nhanviens,
                        'soluong_ban': soluong_ban,
                  })
