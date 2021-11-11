from django.db import models

class Ban(models.Model):
    so_ban = models.CharField(db_column='SO_BAN', primary_key=True, max_length=5)  # Field name made lowercase.
    so_cho_ngoi = models.IntegerField(db_column='SO_CHO_NGOI')  # Field name made lowercase.
    trang_thai = models.CharField(db_column='TRANG_THAI', max_length=50)  # Field name made lowercase.  

    class Meta:
        managed = False
        db_table = 'BAN'


class DatBan(models.Model):
    ma_khach_hang = models.OneToOneField('KhachHang', models.DO_NOTHING, db_column='MA_KHACH_HANG', primary_key=True)  # Field name made lowercase.
    so_ban = models.ForeignKey(Ban, models.DO_NOTHING, db_column='SO_BAN')  # Field name made lowercase.
    thoi_gian = models.DateTimeField(db_column='THOI_GIAN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DAT_BAN'
        unique_together = (('ma_khach_hang', 'so_ban'),)


class DatMon(models.Model):
    ma_hoa_don = models.OneToOneField('HoaDon', models.DO_NOTHING, db_column='MA_HOA_DON', primary_key=True)  # Field name made lowercase.
    ma_mon = models.ForeignKey('MonAn', models.DO_NOTHING, db_column='MA_MON')  # Field name made lowercase.
    so_luong = models.IntegerField(db_column='SO_LUONG')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DAT_MON'
        unique_together = (('ma_hoa_don', 'ma_mon'),)


class HoaDon(models.Model):
    ma_hoa_don = models.CharField(db_column='MA_HOA_DON', primary_key=True, max_length=5)  # Field name made lowercase.
    ma_khach_hang = models.ForeignKey('KhachHang', models.DO_NOTHING, db_column='MA_KHACH_HANG')  # Field name made lowercase.
    ngay_lap = models.DateTimeField(db_column='NGAY_LAP')  # Field name made lowercase.
    don_gia = models.IntegerField(db_column='DON_GIA')  # Field name made lowercase.
    phuong_thuc_thanh_toan = models.CharField(db_column='PHUONG_THUC_THANH_TOAN', max_length=50)  # Field name made lowercase.
    so_ban = models.ForeignKey(Ban, models.DO_NOTHING, db_column='SO_BAN', blank=True, null=True)  # Field name made lowercase.
    ma_nhan_vien = models.ForeignKey('NhanVien', models.DO_NOTHING, db_column='MA_NHAN_VIEN')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HOA_DON'


class KhachHang(models.Model):
    ma_khach_hang = models.CharField(db_column='MA_KHACH_HANG', primary_key=True, max_length=5)  # Field name made lowercase.
    ten_khach_hang = models.CharField(db_column='TEN_KHACH_HANG', max_length=100)  # Field name made lowercase.
    so_dien_thoai = models.CharField(db_column='SO_DIEN_THOAI', max_length=20)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KHACH_HANG'


class Menu(models.Model):
    ma_menu = models.CharField(db_column='MA_MENU', primary_key=True, max_length=5)  # Field name made lowercase.
    ten_menu = models.CharField(db_column='TEN_MENU', max_length=100)  # Field name made lowercase.     

    class Meta:
        managed = False
        db_table = 'MENU'


class MonAn(models.Model):
    ma_mon = models.CharField(db_column='MA_MON', primary_key=True, max_length=5)  # Field name made lowercase.
    ten_mon = models.CharField(db_column='TEN_MON', max_length=100)  # Field name made lowercase.       
    don_vi = models.CharField(db_column='DON_VI', max_length=50)  # Field name made lowercase.
    gia = models.IntegerField(db_column='GIA')  # Field name made lowercase.
    ma_menu = models.ForeignKey(Menu, models.DO_NOTHING, db_column='MA_MENU')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MON_AN'


class NhanVien(models.Model):
    ma_nhan_vien = models.CharField(db_column='MA_NHAN_VIEN', primary_key=True, max_length=5)  # Field name made lowercase.
    ten_nhan_vien = models.CharField(db_column='TEN_NHAN_VIEN', max_length=100)  # Field name made lowercase.
    ngay_sinh = models.DateTimeField(db_column='NGAY_SINH')  # Field name made lowercase.
    gioi_tinh = models.CharField(db_column='GIOI_TINH', max_length=50)  # Field name made lowercase.    
    chuc_vu = models.CharField(db_column='CHUC_VU', max_length=50)  # Field name made lowercase.        
    user = models.CharField(db_column='USER', max_length=100)  # Field name made lowercase.
    password = models.CharField(db_column='PASSWORD', max_length=100)  # Field name made lowercase.     

    class Meta:
        managed = False
        db_table = 'NHAN_VIEN'
    
    def get_user(self):
        return self.user
    def get_password(self):
        return self.password
        
    


class TheThanhVien(models.Model):
    ma_the = models.CharField(db_column='MA_THE', primary_key=True, max_length=5)  # Field name made lowercase.
    ma_khach_hang = models.ForeignKey(KhachHang, models.DO_NOTHING, db_column='MA_KHACH_HANG')  # Field name made lowercase.
    tien_tich_luy = models.IntegerField(db_column='TIEN_TICH_LUY')  # Field name made lowercase.        
    hang = models.CharField(db_column='HANG', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'THE_THANH_VIEN'