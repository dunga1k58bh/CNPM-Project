# Generated by Django 3.2.9 on 2022-01-16 17:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ban',
            fields=[
                ('so_ban', models.IntegerField(db_column='SO_BAN', primary_key=True, serialize=False)),
                ('so_cho_ngoi', models.IntegerField(blank=True, db_column='SO_CHO_NGOI', null=True)),
                ('trang_thai', models.CharField(db_column='TRANG_THAI', max_length=50)),
                ('delete', models.CharField(blank=True, db_column='DELETE', max_length=10, null=True)),
            ],
            options={
                'db_table': 'BAN',
            },
        ),
        migrations.CreateModel(
            name='KhachHang',
            fields=[
                ('ma_khach_hang', models.CharField(db_column='MA_KHACH_HANG', max_length=5, primary_key=True, serialize=False)),
                ('ten_khach_hang', models.CharField(db_column='TEN_KHACH_HANG', max_length=100)),
                ('so_dien_thoai', models.CharField(db_column='SO_DIEN_THOAI', max_length=20)),
            ],
            options={
                'db_table': 'KHACH_HANG',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('ma_menu', models.CharField(db_column='MA_MENU', max_length=5, primary_key=True, serialize=False)),
                ('ten_menu', models.CharField(db_column='TEN_MENU', max_length=100)),
            ],
            options={
                'db_table': 'MENU',
            },
        ),
        migrations.CreateModel(
            name='MonAn',
            fields=[
                ('ma_mon', models.CharField(db_column='MA_MON', max_length=5, primary_key=True, serialize=False)),
                ('ten_mon', models.CharField(db_column='TEN_MON', max_length=100)),
                ('don_vi', models.CharField(db_column='DON_VI', max_length=50)),
                ('gia', models.IntegerField(db_column='GIA')),
                ('dac_biet', models.CharField(db_column='DAC_BIET', max_length=10)),
                ('delete', models.CharField(db_column='DELETE', max_length=10)),
                ('ma_menu', models.ForeignKey(db_column='MA_MENU', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.menu')),
            ],
            options={
                'db_table': 'MON_AN',
            },
        ),
        migrations.CreateModel(
            name='NhanVien',
            fields=[
                ('ma_nhan_vien', models.IntegerField(db_column='MA_NHAN_VIEN', primary_key=True, serialize=False)),
                ('ten_nhan_vien', models.CharField(db_column='TEN_NHAN_VIEN', max_length=100)),
                ('ngay_sinh', models.DateTimeField(db_column='NGAY_SINH')),
                ('gioi_tinh', models.CharField(db_column='GIOI_TINH', max_length=50)),
                ('chuc_vu', models.CharField(db_column='CHUC_VU', max_length=50)),
            ],
            options={
                'db_table': 'NHAN_VIEN',
            },
        ),
        migrations.CreateModel(
            name='TheThanhVien',
            fields=[
                ('ma_the', models.CharField(db_column='MA_THE', max_length=5, primary_key=True, serialize=False)),
                ('tien_tich_luy', models.IntegerField(db_column='TIEN_TICH_LUY')),
                ('hang', models.CharField(db_column='HANG', max_length=50)),
                ('delete', models.CharField(blank=True, db_column='DELETE', max_length=50, null=True)),
                ('tong_tien', models.IntegerField(db_column='TONG_TIEN', null=True)),
                ('ma_khach_hang', models.ForeignKey(db_column='MA_KHACH_HANG', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.khachhang')),
            ],
            options={
                'db_table': 'THE_THANH_VIEN',
            },
        ),
        migrations.CreateModel(
            name='SuKien',
            fields=[
                ('ma_sk', models.AutoField(db_column='MA_SK', primary_key=True, serialize=False)),
                ('ten_sk', models.CharField(db_column='TEN_SK', max_length=50)),
                ('mo_ta', models.CharField(db_column='MO_TA', max_length=200)),
                ('ngay_bd', models.DateTimeField(db_column='NGAY_BD')),
                ('ngay_kt', models.DateTimeField(db_column='NGAY_KT')),
                ('ma_mon', models.ForeignKey(db_column='MA_MON', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.monan')),
            ],
            options={
                'db_table': 'SU_KIEN',
            },
        ),
        migrations.CreateModel(
            name='HoaDon',
            fields=[
                ('ma_hoa_don', models.AutoField(db_column='MA_HOA_DON', primary_key=True, serialize=False)),
                ('ngay_lap', models.DateTimeField(db_column='NGAY_LAP')),
                ('don_gia', models.IntegerField(db_column='DON_GIA')),
                ('phuong_thuc_thanh_toan', models.CharField(db_column='PHUONG_THUC_THANH_TOAN', max_length=50)),
                ('so_ban', models.IntegerField(blank=True, db_column='SO_BAN', null=True)),
                ('tre_em', models.CharField(db_column='TRE_EM', max_length=5, null=True)),
                ('ma_khach_hang', models.ForeignKey(db_column='MA_KHACH_HANG', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.khachhang')),
                ('ma_nhan_vien', models.ForeignKey(db_column='MA_NHAN_VIEN', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.nhanvien')),
            ],
            options={
                'db_table': 'HOA_DON',
            },
        ),
        migrations.CreateModel(
            name='DatBan',
            fields=[
                ('ma_dat_ban', models.AutoField(db_column='MA_DAT_BAN', primary_key=True, serialize=False)),
                ('ho_ten', models.CharField(db_column='HO_TEN', max_length=50)),
                ('sdt', models.CharField(db_column='SDT', max_length=20)),
                ('thoi_gian', models.DateTimeField(db_column='THOI_GIAN')),
                ('so_ban', models.ForeignKey(db_column='SO_BAN', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.ban')),
            ],
            options={
                'db_table': 'DAT_BAN',
            },
        ),
        migrations.AddField(
            model_name='ban',
            name='ma_hoa_don',
            field=models.ForeignKey(blank=True, db_column='MA_HOA_DON', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.hoadon'),
        ),
        migrations.CreateModel(
            name='DatMon',
            fields=[
                ('ma_hoa_don', models.OneToOneField(db_column='MA_HOA_DON', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='restaurant_management.hoadon')),
                ('so_luong', models.IntegerField(db_column='SO_LUONG')),
                ('ma_mon', models.ForeignKey(db_column='MA_MON', on_delete=django.db.models.deletion.DO_NOTHING, to='restaurant_management.monan')),
            ],
            options={
                'db_table': 'DAT_MON',
                'unique_together': {('ma_hoa_don', 'ma_mon')},
            },
        ),
    ]
