import calendar
from datetime import date, datetime, time, timedelta

from django.core.checks import messages
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.views.generic.edit import ModelFormMixin
from django.views.generic.list import ListView
from restaurant_management import models
import json
from django.db.models import Sum
from restaurant_management.form import EventForm
from restaurant_management.utils import CalendarEvent
from django.utils.safestring import mark_safe
from django.db.models.aggregates import Min
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .filter import TTVfilter
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import  User, Group


def group_required(group, login_url=None, raise_exception=False):
    """
    Decorator for views that checks whether a user has a group permission,
    redirecting to the log-in page if necessary.
    If the raise_exception parameter is given the PermissionDenied exception
    is raised.
    """
    def check_perms(user):
        if isinstance(group, str):
            groups = (group, )
        else:
            groups = group
        # First check if the user has the permission (even anon users)

        if user.groups.filter(name__in=groups).exists():
            return True
        # In case the 403 handler should be called raise the exception
        raise PermissionDenied("Tài khoản không có quyền truy cập vào phần này")
        # As the last resort, show the login form
        
    return user_passes_test(check_perms, login_url=login_url)

# from django.http import JsonResponse
# from .models import TheThanhVien
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
            else:
                messages.error(request, "Nhập sai tên đăng nhập hoặc mật khẩu")    
        else:
            messages.error(request, 'Nhập thiếu tên đăng nhập hoặc mật khẩu')
    
    return render(request, "authentication/signin.html", {})


@login_required(login_url='/signin')
def signout(request):
    logout(request)
    return render(request, "authentication/signout.html", {})


@login_required(login_url='/signin')
def home(request):
    bans = models.Ban.objects.filter(delete = 'NO')[1:]
    menu1 = models.MonAn.objects.filter(ma_menu='MN1', delete = 'NO')
    menu2 = models.MonAn.objects.filter(ma_menu='MN2', delete = 'NO')
    menu3 = models.MonAn.objects.filter(ma_menu='MN3', delete = 'NO')
    menu4 = models.MonAn.objects.filter(ma_menu='MN4', delete = 'NO')
    menudb= models.MonAn.objects.filter(dac_biet='YES', delete= 'NO')
    now = timezone.now()
    events = models.SuKien.objects.filter(ngay_bd__lte= now, ngay_kt__gte = now)
    context = {
        'bans': bans,
        'menu1': menu1,
        'menu2': menu2,
        'menu3': menu3,
        'menu4': menu4,
        'menudb': menudb,
        'events': events,
    }
    if "choose_ban" in request.POST :
        so_ban = request.POST.get("choose_ban")
        curban= models.Ban.objects.get(so_ban = 0)
        curban.so_cho_ngoi = so_ban
        curban.save()
        context.update({
            'so_ban':so_ban,
        })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon = ban.ma_hoa_don
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            if hoadon is not None:
                ttte = hoadon.don_gia*0.95
                context.update({
                    'hoadon' : hoadon,
                    'tong_tien_tre_em': ttte,
                    'dat_mons': dat_mons,
                    'dat_bans': dat_bans
                    })
                ban.trang_thai ="busy"
                ban.save()
            if hoadon.ma_khach_hang is not None:
                ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                context.update({
                    'tientichluy' : ma_the.tien_tich_luy,
                    'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                    'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                })       
        except:
            if hoadon is None:
                dat_bans = models.DatBan.objects.filter(so_ban= ban)
                context.update({
                    'dat_bans': dat_bans
                })
                ban.trang_thai ="free"
                ban.save()
    if "add_hoa_don" in request.POST :
        so_ban = request.POST.get("add_hoa_don")
        date = timezone.now()
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")    
        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon=ban.ma_hoa_don
        if hoadon is None:  
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = 0, phuong_thuc_thanh_toan ="tien_mat", so_ban= so_ban, ma_nhan_vien = nhanvien)
            ban.ma_hoa_don= hoadon
        ban.trang_thai ="busy"
        ban.save()
        #  Tìm kiếm thông tin khách hàng
        # ttkh= request.POST.get("thong_tin_khach_hang")
        # try:
        #     ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
        #     hoadon.ma_khach_hang= ma_khach_hang
        #     hoadon.save()
        #     ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
        #     dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        #     context.update({
        #         'tientichluy' : ma_the.tien_tich_luy,
        #         'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
        #         'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
        #     })  
        # except:
        #     hoadon.ma_khach_hang= None
        #     hoadon.save()
        #     context.update({
        #         'tientichluy' : "",
        #         'thongtinkhachhang' : "",
        #         'hotenkhachhang' : "",
        #     }) 
        #Lưu món đặt mới vào csdl
        giahoadon =0 
        ma_hoa_don = hoadon.ma_hoa_don
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            mdds = models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don )
            i =0
            mmm =0
            if so_luong != '0' :
                for mdd in mdds:
                    if ma_mon == mdd.ma_mon.ma_mon :
                        new_so_luong = int(so_luong) + int(mdd.so_luong)
                        mdd.delete()
                        models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = new_so_luong)
                        mmm= ma_mon
                        i=1
                if i==0 :
                    models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)
                else :
                    for mdd in mdds:
                        if mmm != mdd.ma_mon.ma_mon:
                            models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon = mdd.ma_mon, so_luong = mdd.so_luong)
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)
        hoadon.don_gia= hoadon.don_gia + giahoadon 
        # Bàn có trẻ em
        tre_em = request.POST.get("treem_nguoigia")
        if tre_em == "yes":
            hoadon.tre_em=tre_em  
        else :
            hoadon.tre_em= "no"
        hoadon.save()
    if "search_infor_kh" in request.POST:
        so_ban= request.POST.get("search_infor_kh")
        ttkh= request.POST.get("thong_tin_khach_hang")
        ban = models.Ban.objects.get(so_ban = so_ban)
        hoadon=ban.ma_hoa_don
        try:          
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            hoadon.ma_khach_hang= ma_khach_hang
            hoadon.save()
        except:
            hoadon.ma_khach_hang= None
            hoadon.save()
        tre_em = request.POST.get("treem_nguoigia")
        if tre_em == "yes":
            hoadon.tre_em=tre_em  
        else :
            hoadon.tre_em= "no"
        hoadon.save()
    if "tieu_tich_luy" in request.POST:
        so_ban= request.POST.get("tieu_tich_luy")
        sodiemtieu = request.POST.get("so_diem_tieu")
        ttkh= request.POST.get("thong_tin_khach_hang")
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
            so_diem_tieu = int(sodiemtieu)
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = ma_khach_hang)
            thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy- so_diem_tieu
            hoadon.don_gia = hoadon.don_gia - int(sodiemtieu)
            hoadon.save()
            thethanhvien.save()
        except:
            print("Thất bại trong tiêu tích lũy")   
        tre_em = request.POST.get("treem_nguoigia")
        if tre_em == "yes":
            hoadon.tre_em=tre_em  
        else :
            hoadon.tre_em= "no"
        hoadon.save()    
    if "remove_hoa_don" in request.POST :
        ma_hoa_don = request.POST.get("remove_hoa_don")
        hoadon= models.HoaDon.objects.get(ma_hoa_don=ma_hoa_don)
        so_ban = hoadon.so_ban
        ban=models.Ban.objects.get(so_ban=so_ban)
        models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don).delete()
        ban.ma_hoa_don = None
        ban.trang_thai="free"
        ban.save()
        hoadon.delete()    
    #Khi click thanh toán thì xóa hóa đơn khỏi bàn trả về bàn chưa có hóa đơn     
    if "pay_hoa_don" in request.POST :
        ma_hoa_don = request.POST.get("pay_hoa_don")
        hoadon= models.HoaDon.objects.get(ma_hoa_don=ma_hoa_don)
        tre_em = request.POST.get("treem_nguoigia")
        if tre_em == "yes":
            hoadon.tre_em=tre_em  
        else :
            hoadon.tre_em= "no"
        hoadon.save()
        if hoadon.tre_em == "yes":
            hoadon.don_gia = hoadon.don_gia*0.95
            hoadon.save()
        so_ban = hoadon.so_ban
        ban=models.Ban.objects.get(so_ban=so_ban)
        ma_hoa_don = hoadon.ma_hoa_don
        ban.ma_hoa_don = None
        ban.trang_thai= "free"
        ban.save()  
        try:
            if hoadon.ma_khach_hang is not None:             
                thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                thethanhvien.tong_tien= thethanhvien.tong_tien+ hoadon.don_gia
                tong_tien = thethanhvien.tong_tien
                heso = 0.1
                if tong_tien > 50000000:
                    thethanhvien.hang = 'Kim cương'
                    heso = 0.25
                elif tong_tien > 30000000 :
                    thethanhvien.hang = 'Vàng'
                    heso = 0.2
                elif tong_tien > 10000000:
                    thethanhvien.hang ='Bạc'
                    heso =0.15
                else :
                    thethanhvien.hang = 'Đồng'                       
                thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy + hoadon.don_gia * heso
                thethanhvien.save()
        except:
            print("Hóa đơn này không có mã khách hàng!")
    # 
    curban = models.Ban.objects.get(so_ban=0)
    ncurban= curban.so_cho_ngoi
    if ncurban != 0:
        so_ban = ncurban
        context.update({
            'so_ban':so_ban,
        })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon = ban.ma_hoa_don
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            if hoadon is not None:
                tt = int(hoadon.don_gia*0.95)
                context.update({
                    'hoadon' : hoadon,
                    'tong_tien_tre_em': tt,
                    'dat_mons': dat_mons,
                    'dat_bans': dat_bans
                })
                ban.trang_thai ="busy"
                ban.save()
            if hoadon.ma_khach_hang is not None:
                ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                context.update({
                    'tientichluy' : ma_the.tien_tich_luy,
                    'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                    'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                })           
        except:
            if hoadon is None:
                dat_bans = models.DatBan.objects.filter(so_ban= ban)
                context.update({
                    'hoadon' : hoadon,
                    'dat_mons': None,
                    'dat_bans': dat_bans
                    })
                ban.trang_thai ="free"
                ban.save()
    #
    return render(request, "management/home.html", context)

@login_required(login_url='/signin')
def booking (request):
    bans = models.Ban.objects.filter(delete = 'NO')[1:]
    context = {
        'bans': bans,
    }
    if "choose_ban" in request.POST :
        so_ban = request.POST.get("choose_ban")
        curban= models.Ban.objects.get(so_ban = 0)
        curban.so_cho_ngoi = so_ban
        curban.save()
        context.update({
            'so_ban':so_ban
        })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            print(dat_bans)
            context.update({
                'dat_bans': dat_bans
            })
            ban.save()
        except:
            print("Bàn này chưa có khách đặt!")
            ban.save()
    if "booking_table" in request.POST :
        so_ban = request.POST.get("booking_table")
        ban = models.Ban.objects.get(so_ban = so_ban)
        ho_ten = request.POST.get("ho_ten")
        sdt = request.POST.get("sdt")
        date = request.POST.get("thoi_gian")
        dat_ban= models.DatBan.objects.create(ho_ten = ho_ten, sdt = sdt, so_ban = ban, thoi_gian = date)
    if "delete_booking" in request.POST :
        ma_dat_ban = request.POST.get("delete_booking")
        dat_ban = models.DatBan.objects.get(ma_dat_ban = ma_dat_ban )
        dat_ban.delete()
    # 
    curban = models.Ban.objects.get(so_ban=0)
    ncurban= curban.so_cho_ngoi
    if ncurban != 0:
        so_ban = ncurban
        context.update({
            'so_ban':so_ban,
        })
        try:
            ban = models.Ban.objects.get(so_ban = so_ban)
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            context.update({
                'dat_bans': dat_bans
            })     
        except:
            context.update({
                'dat_bans': dat_bans
            })  
            print("Bàn này chưa có lịch đặt!")
    #
    return render(request, "management/booking.html", context)

@login_required(login_url='/signin')
def takeAway(request):
    menu1 = models.MonAn.objects.filter(ma_menu='MN1', delete = 'NO')
    menu2 = models.MonAn.objects.filter(ma_menu='MN2', delete = 'NO')
    menu3 = models.MonAn.objects.filter(ma_menu='MN3', delete = 'NO')
    menu4 = models.MonAn.objects.filter(ma_menu='MN4', delete = 'NO')
    menudb= models.MonAn.objects.filter(dac_biet='YES',delete = 'NO')
    ban= models.Ban.objects.get(so_ban=0)
    context = {
        'menu1': menu1,
        'menu2': menu2,
        'menu3': menu3,
        'menu4': menu4,
        'menudb': menudb,
    }
    try:
        hoadon = ban.ma_hoa_don
        dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        if hoadon is not None:
            context.update({
                'hoadon' : hoadon,
                'tongtien': hoadon.don_gia,
                'dat_mons': dat_mons,
                'mahoadon':hoadon.ma_hoa_don,
                })
            ban.save()
            if hoadon.ma_khach_hang is not None:
                ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                context.update({
                    'tientichluy' : ma_the.tien_tich_luy,
                    'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                    'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                })     
    except:
        print("Chưa có hóa đơn!")
    # Tương ứng bên giao diện là lưu hóa đơn, khi click thì tạo hóa đơn và lưu, mặc định số bàn là 8
    if "add_hoa_don" in request.POST :    
        ma_hoa_don = request.POST.get("add_hoa_don")
        date = timezone.now()
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)
        giahoadon =0  
        if ma_hoa_don != '':  
            hoadon = models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        else:          
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = giahoadon, phuong_thuc_thanh_toan ="tien_mat",so_ban= 0,  ma_nhan_vien = nhanvien)  
            ma_hoa_don= hoadon.ma_hoa_don
            ban.ma_hoa_don= hoadon
            ban.save()
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            mdds = models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don )
            i =0
            mmm =0
            if so_luong != '0' :
                for mdd in mdds:
                    if ma_mon == mdd.ma_mon.ma_mon :
                        new_so_luong = int(so_luong) + int(mdd.so_luong)
                        mdd.delete()
                        models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = new_so_luong)
                        mmm= ma_mon
                        i=1
                if i==0 :
                    models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon= mon_an, so_luong = so_luong)
                else :
                    for mdd in mdds:
                        if mmm != mdd.ma_mon.ma_mon:
                            models.DatMon.objects.create(ma_hoa_don = hoadon, ma_mon = mdd.ma_mon, so_luong = mdd.so_luong)
            giahoadon = giahoadon +  int(so_luong)* int(mon_an.gia)
        hoadon.don_gia = hoadon.don_gia + giahoadon
        hoadon.save()
        dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        context.update({
            'mahoadon' : hoadon.ma_hoa_don ,
            'tongtien' : hoadon.don_gia,
            'dat_mons': dat_mons ,
        })
        # ttkh= request.POST.get("thong_tin_khach_hang")
        # try:
        #     ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
        #     hoadon.ma_khach_hang= ma_khach_hang
        #     hoadon.save()
        #     ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
        #     dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        #     context.update({
        #         'tientichluy' : ma_the.tien_tich_luy,
        #         'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
        #         'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
        #     })  
        # except:
        #     hoadon.ma_khach_hang= None
        #     hoadon.save()
        #     context.update({
        #         'tientichluy' : "",
        #         'thongtinkhachhang' : "",
        #         'hotenkhachhang' : "",
        #     })
        #     print("Không tìm thấy thông tin khách hàng trong CSDL!")

    if "search_infor_kh" in request.POST:
        mahoadon = request.POST.get("search_infor_kh")
        try:
            hoadon=models.HoaDon.objects.get(ma_hoa_don = mahoadon)
            ttkh= request.POST.get("thong_tin_khach_hang")
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            hoadon.ma_khach_hang= ma_khach_hang
            hoadon.save()
            ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            context.update({
                'tientichluy' : ma_the.tien_tich_luy,
                'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                'mahoadon' : hoadon.ma_hoa_don ,
                'tongtien' : hoadon.don_gia,
                'dat_mons': dat_mons ,
            })
        except:
            hoadon.ma_khach_hang= None
            hoadon.save()
            context.update({
                'tientichluy' : "",
                'thongtinkhachhang' : "",
                'hotenkhachhang' : "",
            })
            print("Không tìm thấy thông tin khách hàng trong CSDL!")
    if "tieu_tich_luy" in request.POST:
        mahoadon = request.POST.get("tieu_tich_luy")
        try:
            hoadon=models.HoaDon.objects.get(ma_hoa_don = mahoadon)
            sodiemtieu = request.POST.get("so_diem_tieu")
            ttkh= request.POST.get("thong_tin_khach_hang")
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = ma_khach_hang)
            thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy- int(sodiemtieu)
            hoadon.don_gia = hoadon.don_gia - int(sodiemtieu)
            hoadon.save()
            thethanhvien.save()
            ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            context.update({
                'tientichluy' : ma_the.tien_tich_luy,
                'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                'mahoadon' : hoadon.ma_hoa_don ,
                'tongtien' : hoadon.don_gia,
                'dat_mons': dat_mons ,
            })
        except:
            print("Thất bại trong tiêu tích lũy!")
    # Xóa hóa đơn
    if "remove_hoa_don" in request.POST :
        ban= models.Ban.objects.get(so_ban=0)
        ma_hoa_don= request.POST.get("remove_hoa_don")
        hoadon= models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        ban.ma_hoa_don=None
        ban.save()
        models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don).delete()
        hoadon.delete()
        context.update({
            'mahoadon' : "",
            'tongtien' :"",
            'dat_mons': "",
            'tientichluy' : "",
            'thongtinkhachhang' : "",
            'hotenkhachhang' : "",
        })
    # Thanh toán hóa đơn
    if "pay_hoa_don" in request.POST:
        ban= models.Ban.objects.get(so_ban=0)
        ban.ma_hoa_don=None
        ban.save()
        ma_hoa_don= request.POST.get("pay_hoa_don")
        hoadon= models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        if hoadon.tre_em == "yes":
            hoadon.tong_tien = hoadon.tong_tien*0.95
            hoadon.save()
        ma_hoa_don = hoadon.ma_hoa_don
        context.update({
                'mahoadon' : "",
                'tongtien' :"",
                'dat_mons': "",
                'tientichluy' : "",
                'thongtinkhachhang' : "",
                'hotenkhachhang' : "",
            })
        try:
            if hoadon.ma_khach_hang is not None:               
                thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                thethanhvien.tong_tien= thethanhvien.tong_tien+ hoadon.don_gia
                tong_tien = thethanhvien.tong_tien
                heso = 0.1
                if tong_tien > 50000000:
                    thethanhvien.hang = 'Kim cương'
                    heso = 0.25
                elif tong_tien > 30000000 :
                    thethanhvien.hang = 'Vàng'
                    heso = 0.2
                elif tong_tien > 10000000:
                    thethanhvien.hang ='Bạc'
                    heso =0.15
                else :
                    thethanhvien.hang = 'Đồng'       
                thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy + hoadon.don_gia * heso
                thethanhvien.save()
        except:
                print("Hóa đơn này chưa có mã khách hàng")
    return render(request, "management/take_away.html", context)

class EventsView(LoginRequiredMixin, ListView, ModelFormMixin):
    login_url = '/signin'
    model = models.SuKien
    template_name='calendar_event/events.html'
    form_class = EventForm
    group_required = u"quản trị viên"
    
    def get(self, request, *args, **kwargs):
        self.object = None
        self.form = self.form_class()
        # Explicitly states what get to call:
        return ListView.get(self, request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        self.object = None
        self.form = self.get_form(self.form_class)
        if self.form.is_valid():
            self.object = self.form.save()
        if "delete_event" in request.POST :
            ma_sk = request.POST.get("delete_event")
            event_del = models.SuKien.objects.get(ma_sk = ma_sk)
            event_del.delete()
        return self.get(request, *args, **kwargs)
            
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('day', None))
        d = get_date(self.request.GET.get('month', None))
        print(d)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        cal_event = CalendarEvent(d.year, d.month)
        html_cal = cal_event.formatmonth(withyear=True)
        context['calendar_event'] = mark_safe(html_cal)
        create_event_form = self.form
        context["create_event_form"] = create_event_form
        events = models.SuKien.objects.filter(ngay_bd__month=d.month,
                                              ngay_bd__year__lte= d.year)
        context["events"] = events
        return context

    
    
    
def get_date(req_day):
    if req_day :
        year, month = (int(x) for  x in req_day.split('-'))
        return date(year, month, day=1) 
    return datetime.today()    
def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month   

    
    
    
    
@login_required(login_url='/signin')
def vipMember(request):
    
    if 'AddKH' in request.POST:
        # KH_Hang = request.POST.get("AddKH")
        # Member = models.KhachHang.objects.get(KH_Hang = KH_Hang)
        ma_the = request.POST.get('so_dien_thoai')
        ma_khach_hang = request.POST.get('so_dien_thoai')
        ten_khach_hang = request.POST.get('ten_khach_hang')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        try:
            KH = models.KhachHang.objects.create(ma_khach_hang = ma_khach_hang, ten_khach_hang = ten_khach_hang, so_dien_thoai = so_dien_thoai)  
            models.TheThanhVien.objects.create(ma_the = ma_the, ma_khach_hang = KH, tien_tich_luy = 0, tong_tien=0, hang = 'Đồng')
        except:
            #html = '<script>alert("Không thành công")</script>'
            #messages.error(request, 'Không thành công')
            return redirect('/vip_member/')
    if 'DelKH' in request.POST:
        ma_the = request.POST.get('DelKH')
        the = models.TheThanhVien.objects.get(ma_the = ma_the)
        the.delete = 'yes'
        the.save()
    menus = models.Menu.objects.all()
    thethanhviens = models.TheThanhVien.objects.filter(delete__isnull = True)
    myFilter = TTVfilter(request.GET, queryset=thethanhviens)
    thethanhviens = myFilter.qs
    context = {
        'menu' : menus,
        'thethanhviens' : thethanhviens,
        'myFilter' : myFilter,
        # 'khachhangs' : khachhangs,
        # 'KH_Hang' : KH_Hang
    }
    return render(request, "management/vip_member.html", context)
# def checkNickName(request):
#     # request should be ajax and method should be GET.
#     if request.is_ajax and request.method == "GET":
#         # get the nick name from the client side.
#         ma_the = request.GET.get("ma_the", None)
#         # check for the nick name in the database.
#         if TheThanhVien.objects.filter(ma_the = ma_the).exists():
#             # if nick_name found return not valid new friend
#             return JsonResponse({"valid":False}, status = 200)
#         else:
#             # if nick_name not found, then user can create a new friend.
#             return JsonResponse({"valid":True}, status = 200)

#     return JsonResponse({}, status = 400)

@login_required(login_url='/signin')
@group_required('quản trị viên',login_url='/')
def statistics(request):
    context = {}
    # lay thong tin cho tab all
    ma_mons_all = []
    so_luong_mons_all = []
    ten_mons_all = []
    dat_mons_all = models.DatMon.objects.all().values('ma_mon').annotate(Sum('so_luong'))
    if dat_mons_all:
        for dat_mon_all in dat_mons_all:
            ma_mons_all.append(dat_mon_all['ma_mon'])
            so_luong_mons_all.append(dat_mon_all['so_luong__sum'])
    for ma_mon_all in ma_mons_all:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_all)
        for mon in mons:
            ten_mons_all.append(mon.ten_mon)
    context.update({
        'ten_mons_all': json.dumps(ten_mons_all),
        'so_luong_mons_all': json.dumps(so_luong_mons_all),
    })
    ma_menus_all = []
    ten_menus_all = []
    so_luong_menus_all = []
    for ma_mon_all in ma_mons_all:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_all)
        if mons:
            for mon in mons:
                if mon.ma_menu.ma_menu not in ma_menus_all:
                    ma_menus_all.append(mon.ma_menu.ma_menu)
                    ten_menus_all.append(mon.ma_menu.ten_menu)
    for ma_menu_all in ma_menus_all:
        count = 0
        dat_mons = models.DatMon.objects.filter(ma_mon__ma_menu=ma_menu_all).values('ma_mon').annotate(Sum('so_luong'))
        if dat_mons:
            for dat_mon in dat_mons:
                count += dat_mon['so_luong__sum']
            so_luong_menus_all.append(count)
    context.update({
        'ten_menus_all': json.dumps(ten_menus_all),
        'so_luong_menus_all': json.dumps(so_luong_menus_all),
    })


    doanh_thu_all = []
    years = []
    year_min = models.HoaDon.objects.aggregate(Min('ngay_lap__year'))['ngay_lap__year__min']
    if year_min is None:
        year_min = timezone.now().year
    for year_idx in range(year_min, timezone.now().year + 1):
        years.append(year_idx)
        doanh_thu_year = 0
        hoa_dons_year = models.HoaDon.objects.filter(ngay_lap__year=year_idx)
        if hoa_dons_year:
            for hoa_don_year in hoa_dons_year:
                doanh_thu_year += hoa_don_year.don_gia
        doanh_thu_all.append(doanh_thu_year)
    tong_doanh_thu_all = 0
    for i in doanh_thu_all:
        tong_doanh_thu_all += i
    context.update({
        'doanh_thu_all': json.dumps(doanh_thu_all),
        'years': json.dumps(years),
        'tong_doanh_thu_all': tong_doanh_thu_all,
    })

    
    #############################################################
    # lay thong tin cho tab year
    ma_mons_year = []
    so_luong_mons_year = []
    ten_mons_year = []
    dat_mons_year = models.DatMon.objects.filter(ma_hoa_don__ngay_lap__year=timezone.now().year).values('ma_mon').annotate(Sum('so_luong'))
    if dat_mons_year:
        for dat_mon_year in dat_mons_year:
            ma_mons_year.append(dat_mon_year['ma_mon'])
            so_luong_mons_year.append(dat_mon_year['so_luong__sum'])
    for ma_mon_year in ma_mons_year:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_year)
        for mon in mons:
            ten_mons_year.append(mon.ten_mon)
    context.update({
        'ten_mons_year': json.dumps(ten_mons_year),
        'so_luong_mons_year': json.dumps(so_luong_mons_year),
    })
    ma_menus_year = []
    ten_menus_year = []
    so_luong_menus_year = []
    for ma_mon_year in ma_mons_year:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_year)
        if mons:
            for mon in mons:
                if mon.ma_menu.ma_menu not in ma_menus_year:
                    ma_menus_year.append(mon.ma_menu.ma_menu)
                    ten_menus_year.append(mon.ma_menu.ten_menu)
    for ma_menu_year in ma_menus_year:
        count = 0
        dat_mons = models.DatMon.objects.filter(ma_mon__ma_menu=ma_menu_year).values('ma_mon').annotate(Sum('so_luong'))
        if dat_mons:
            for dat_mon in dat_mons:
                count += dat_mon['so_luong__sum']
            so_luong_menus_year.append(count)
    context.update({
        'ten_menus_year': json.dumps(ten_menus_year),
        'so_luong_menus_year': json.dumps(so_luong_menus_year),
    })


    doanh_thu_year = []
    months = []
    for month_idx in range(1, timezone.now().month + 1):
        months.append(month_idx)
        doanh_thu_month = 0
        hoa_dons_month = models.HoaDon.objects.filter(ngay_lap__month=month_idx,
                                                      ngay_lap__year=timezone.now().year)
        if hoa_dons_month:
            for hoa_don_month in hoa_dons_month:
                doanh_thu_month += hoa_don_month.don_gia
        doanh_thu_year.append(doanh_thu_month)
    tong_doanh_thu_year = 0
    for i in doanh_thu_year:
        tong_doanh_thu_year += i
    context.update({
        'doanh_thu_year': json.dumps(doanh_thu_year),
        'months': json.dumps(months),
        'tong_doanh_thu_year': tong_doanh_thu_year,
    })
    

    #############################################################
    # lay thong tin cho tab month
    ma_mons_month = []
    so_luong_mons_month = []
    ten_mons_month = []
    dat_mons_month = models.DatMon.objects.filter(ma_hoa_don__ngay_lap__month=timezone.now().month,
                                                  ma_hoa_don__ngay_lap__year=timezone.now().year).values('ma_mon').annotate(Sum('so_luong'))
    if dat_mons_month:
        for dat_mon_month in dat_mons_month:
            ma_mons_month.append(dat_mon_month['ma_mon'])
            so_luong_mons_month.append(dat_mon_month['so_luong__sum'])
    for ma_mon_month in ma_mons_month:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_month)
        if mons:
            for mon in mons:
                ten_mons_month.append(mon.ten_mon)
    context.update({
        'ten_mons_month': json.dumps(ten_mons_month),
        'so_luong_mons_month': json.dumps(so_luong_mons_month),
    })
    ma_menus_month = []
    ten_menus_month = []
    so_luong_menus_month = []
    for ma_mon_month in ma_mons_month:
        mons = models.MonAn.objects.filter(ma_mon=ma_mon_month)
        if mons:
            for mon in mons:
                if mon.ma_menu.ma_menu not in ma_menus_month:
                    ma_menus_month.append(mon.ma_menu.ma_menu)
                    ten_menus_month.append(mon.ma_menu.ten_menu)
    for ma_menu_month in ma_menus_month:
        count = 0
        dat_mons = models.DatMon.objects.filter(ma_mon__ma_menu=ma_menu_month).values('ma_mon').annotate(Sum('so_luong'))
        if dat_mons:
            for dat_mon in dat_mons:
                count += dat_mon['so_luong__sum']
            so_luong_menus_month.append(count)
    context.update({
        'ten_menus_month': json.dumps(ten_menus_month),
        'so_luong_menus_month': json.dumps(so_luong_menus_month),
    })


    doanh_thu_month = []
    days = []
    for day_idx in range(1, timezone.now().day + 1):
        days.append(day_idx)
        doanh_thu_day = 0
        hoa_dons_day = models.HoaDon.objects.filter(ngay_lap__day=day_idx,
                                                    ngay_lap__month=timezone.now().month,
                                                    ngay_lap__year=timezone.now().year)
        if hoa_dons_day:
            for hoa_don_day in hoa_dons_day:
                doanh_thu_day += hoa_don_day.don_gia
        doanh_thu_month.append(doanh_thu_day)
    tong_doanh_thu_month = 0
    for i in doanh_thu_month:
        tong_doanh_thu_month += i
    context.update({
        'doanh_thu_month': json.dumps(doanh_thu_month),
        'days': json.dumps(days),
        'tong_doanh_thu_month': tong_doanh_thu_month,
    })


    #############################################################
    return render(request, "management/statistics.html", context)


@login_required(login_url='/signin')
@group_required('quản trị viên',login_url='/')
def setting(request):
    menus = models.Menu.objects.all()
    monans = models.MonAn.objects.filter(delete = 'NO') 
    bans = models.Ban.objects.filter(delete = 'NO') 
    nhanviens = models.NhanVien.objects.all() 
    mondacbiet = models.MonAn.objects.filter(dac_biet = 'YES',delete = 'NO' )
    quanly = models.NhanVien.objects.filter(ma_nhan_vien = '1' )
    if "save_mon" in request.POST :
        name_mon = request.POST.get("tenmonan")
        gia_mon = request.POST.get("giamonan")
        don_vi_mon = request.POST.get("donvimon")
        count_mon = (models.MonAn.objects.filter().count()+1)
        ma_menu = request.POST.get("save_mon")
        menu_moi = models.Menu.objects.get(ma_menu = ma_menu)
        if  name_mon != "" and don_vi_mon != "":
            models.MonAn.objects.create(ma_mon = "M"+str(count_mon), ten_mon = name_mon, don_vi = don_vi_mon, gia = gia_mon, ma_menu = menu_moi, delete = 'NO')
        ma_mon_sua = request.POST.getlist("ma_monss")
        gia_sua = request.POST.getlist("giamonsua")
        for ma_mon in ma_mon_sua:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            gia_moi = gia_sua[ma_mon_sua.index(ma_mon)]
            mon_an.gia = gia_moi
            mon_an.save()
    if "save_db" in request.POST :
        list_add_db = request.POST.getlist("list_add")
        for monan in monans:
            monan.dac_biet = "NO"
            for add_db in list_add_db:
                if monan.ma_mon == add_db :
                    monan.dac_biet = "YES"
            monan.save()
    if "xoa_mon" in request.POST :
        ma_mon_xoa=request.POST.get("xoa_mon")
        mon_xoa = models.MonAn.objects.get(ma_mon = ma_mon_xoa)
        mon_xoa.delete = "YES"
        mon_xoa.save()
    if "save_ban" in request.POST :
        banall = models.Ban.objects.all()
        so_ban_sua = int(request.POST.get("quantity"))
        for ban in banall :
            if ban.so_ban <=so_ban_sua :
                ban.delete = "NO"
                ban.save()
            else :
                ban.delete = "YES"
                ban.save()
    soluong_ban = (models.Ban.objects.filter(delete = 'NO').count() -1)
    groups = Group.objects.values('id', 'name')
    user_array = []
    group_array = []
    for group in groups:
        group_ = Group.objects.get(id=group['id'])
        users_group = group_.user_set.filter(is_superuser=False)
        if users_group:
            for user_group in users_group:
                user_array.append(user_group)
                group_array.append(group['name'])
    users = zip(user_array, group_array)

    return render(request, "management/setting.html",
                  {
                        'users': users,
                        'menus' : menus,
                        'monans' : monans,
                        'bans' : bans,
                        'nhanviens' : nhanviens,
                        'soluong_ban': soluong_ban,
                        'mondacbiet': mondacbiet,
                        'quanly': quanly
                  })
