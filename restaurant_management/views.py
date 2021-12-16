import calendar
from datetime import date, datetime, time, timedelta
from django.core.checks import messages
from django.http.response import HttpResponse
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
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            if hoadon is not None:
                context.update({
                    'hoadon' : hoadon,
                    'dat_mons': dat_mons,
                    'dat_bans': dat_bans
                    })
                ban.trang_thai ="đang sử dụng"
                ban.save()
            if hoadon.ma_khach_hang is not None:
                ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                # hoadon.ma_khach_hang= None
                # hoadon.save()
                context.update({
                    'tientichluy' : ma_the.tien_tich_luy,
                    'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                    'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
                })
                
        except:
            if hoadon is None:
                print("ban nay chua co hoa don")
                dat_bans = models.DatBan.objects.filter(so_ban= ban)
                context.update({
                    'dat_bans': dat_bans
                    })
                ban.trang_thai ="rảnh"
                ban.save()
    if "add_hoa_don" in request.POST :
        # Đoạn này để tạo hóa đơn và thêm hóa đơn vào bàn
        so_ban = request.POST.get("add_hoa_don")
        date = timezone.now()
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)

        # Lấy ra danh sách mã món đã thêm và số lượng để add vào bảng Đặt món
        
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            hoadon.ma_khach_hang= ma_khach_hang
            hoadon.save()
        else :
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
           
        
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
    if "search_infor_kh" in request.POST:
        so_ban= request.POST.get("search_infor_kh")
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            hoadon.ma_khach_hang= ma_khach_hang
            hoadon.save()
        else :
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
            hoadon.ma_khach_hang= None
            hoadon.save()
    if "tieu_tich_luy" in request.POST:
        so_ban= request.POST.get("tieu_tich_luy")
        sodiemtieu = request.POST.get("so_diem_tieu")
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
            ban = models.Ban.objects.get(so_ban = so_ban)
            hoadon=ban.ma_hoa_don
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = ma_khach_hang)
            thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy- int(sodiemtieu)
            hoadon.don_gia = hoadon.don_gia - int(sodiemtieu)
            hoadon.save()
            thethanhvien.save()
            
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
            if hoadon.ma_khach_hang is not None:               
                thethanhvien = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
                thethanhvien.tien_tich_luy = thethanhvien.tien_tich_luy + hoadon.don_gia * 0.1
                thethanhvien.save()
    
    if "booking_table" in request.POST :
        so_ban = request.POST.get("booking_table")
        ban = models.Ban.objects.get(so_ban = so_ban)
        ho_ten = request.POST.get("ho_ten")
        sdt = request.POST.get("sdt")
        date = request.POST.get("thoi_gian")
        dat_ban= models.DatBan.objects.create(ho_ten = ho_ten, sdt = sdt, so_ban = ban, thoi_gian = date)

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
            dat_bans = models.DatBan.objects.filter(so_ban= ban)
            print(dat_bans)
            #if dat_bans is not None:
            context.update({
                    'dat_bans': dat_bans
                    })
            #ban.trang_thai ="đang đợi"
            ban.save()
        except:
            print("ban nay chua co khach dat")
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
        print(dat_ban)
        dat_ban.delete()

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
        date = timezone.now()
        ma_mon_dat = request.POST.getlist("ma_mons")
        so_luong_dat = request.POST.getlist("so_luongs")
        nhanvien = models.NhanVien.objects.get(ma_nhan_vien = 1)
        giahoadon =0  
        
        if ma_hoa_don != '':  
            hoadon = models.HoaDon.objects.get(ma_hoa_don = ma_hoa_don)
        else:          
            hoadon = models.HoaDon.objects.create(ngay_lap = date, don_gia = giahoadon, phuong_thuc_thanh_toan ="tien_mat",so_ban= 8,  ma_nhan_vien = nhanvien)  
            ma_hoa_don= hoadon.ma_hoa_don
        for ma_mon in ma_mon_dat:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            so_luong = so_luong_dat[ma_mon_dat.index(ma_mon)]
            #
            mdds = models.DatMon.objects.filter(ma_hoa_don = ma_hoa_don )
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
        hoadon.don_gia = hoadon.don_gia + giahoadon
        hoadon.save()
        dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
        context.update({
            'mahoadon' : hoadon.ma_hoa_don ,
            'tongtien' : hoadon.don_gia,
            'dat_mons': dat_mons ,
        })
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
            ma_khach_hang= models.KhachHang.objects.get(so_dien_thoai = ttkh)
            hoadon.ma_khach_hang= ma_khach_hang
            hoadon.save()
            ma_the = models.TheThanhVien.objects.get(ma_khach_hang = hoadon.ma_khach_hang)
            dat_mons = models.DatMon.objects.filter(ma_hoa_don = hoadon.ma_hoa_don)
            context.update({
                'tientichluy' : ma_the.tien_tich_luy,
                'thongtinkhachhang' : hoadon.ma_khach_hang.so_dien_thoai,
                'hotenkhachhang' : hoadon.ma_khach_hang.ten_khach_hang,
            })  
    if "search_infor_kh" in request.POST:
        mahoadon = request.POST.get("search_infor_kh")
        hoadon=models.HoaDon.objects.get(ma_hoa_don = mahoadon)
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
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
    if "tieu_tich_luy" in request.POST:
        mahoadon = request.POST.get("tieu_tich_luy")
        hoadon=models.HoaDon.objects.get(ma_hoa_don = mahoadon)
        sodiemtieu = request.POST.get("so_diem_tieu")
        ttkh= request.POST.get("thong_tin_khach_hang")
        if ttkh != "":
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

class EventsView(ListView, ModelFormMixin):
    model = models.SuKien
    template_name='calendar_event/events.html'
    form_class = EventForm
    
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
        events = models.SuKien.objects.filter(ngay_bd__month__lte= d.month, ngay_kt__month__gte=d.month,
                                              ngay_bd__year__lte= d.year, ngay_kt__year__gte=d.year)
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

    
    
    
    
    
def vipMember(request):
    
    if 'AddKH' in request.POST:
        # KH_Hang = request.POST.get("AddKH")
        # Member = models.KhachHang.objects.get(KH_Hang = KH_Hang)
        ma_the = request.POST.get('ma_the')
        ma_khach_hang = request.POST.get('ma_khach_hang')
        ten_khach_hang = request.POST.get('ten_khach_hang')
        so_dien_thoai = request.POST.get('so_dien_thoai')
        try:
            KH = models.KhachHang.objects.create(ma_khach_hang = ma_khach_hang, ten_khach_hang = ten_khach_hang, so_dien_thoai = so_dien_thoai)  
            models.TheThanhVien.objects.create(ma_the = ma_the, ma_khach_hang = KH, tien_tich_luy = 0, hang = 'Đồng')
        except:
            print('Không được')
    if 'DelKH' in request.POST:
        ma_the = request.POST.get('DelKH')
        the = models.TheThanhVien.objects.get(ma_the = ma_the)
        the.delete = 'yes'
        the.save()
    menus = models.Menu.objects.all()
    thethanhviens = models.TheThanhVien.objects.filter(delete__isnull = True)
    context = {
        'menu' : menus,
        'thethanhviens' : thethanhviens,
        # 'khachhangs' : khachhangs,
        # 'KH_Hang' : KH_Hang
    }
    return render(request, "management/vip_member.html", context)


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


def setting(request):
    menus = models.Menu.objects.all()
    monans = models.MonAn.objects.all() 
    bans = models.Ban.objects.all() 
    nhanviens = models.NhanVien.objects.all() 
    soluong_ban = models.Ban.objects.filter().count() 
    
    if "save_mon" in request.POST :
        name_mon = request.POST.get("tenmonan")
        gia_mon = request.POST.get("giamonan")
        don_vi_mon = request.POST.get("donvimon")
        count_mon = (models.MonAn.objects.filter().count()+1)
        ma_menu = request.POST.get("save_mon")
        menu_moi = models.Menu.objects.get(ma_menu = ma_menu)
        if name_mon != "Thêm món" and name_mon != "" and don_vi_mon != "Đơn vị" and don_vi_mon != "":
            mon_moi = models.MonAn.objects.create(ma_mon = "M"+str(count_mon), ten_mon = name_mon, don_vi = don_vi_mon, gia = gia_mon, ma_menu = menu_moi)
            mon_moi.save()
        ma_mon_sua = request.POST.getlist("ma_monss")
        gia_sua = request.POST.getlist("giamonsua")
        for ma_mon in ma_mon_sua:
            mon_an = models.MonAn.objects.get(ma_mon = ma_mon)
            gia_moi = gia_sua[ma_mon_sua.index(ma_mon)]
            mon_an.gia = gia_moi
            mon_an.save()
    return render(request, "management/setting.html", 
                  {
                        'menus' : menus,
                        'monans' : monans,
                        'bans' : bans,
                        'nhanviens' : nhanviens,
                        'soluong_ban': soluong_ban,
                  })
