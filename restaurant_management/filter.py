from django.db.models import fields
from django_filters import DateFromToRangeFilter, DateFilter, CharFilter, NumberFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
import django_filters

from .models import *

class TTVfilter(django_filters.FilterSet):
    #name = django_filters.CharFilter(lookup_expr='iexact')
    ma_the = CharFilter(label='SĐT')
    hang = CharFilter(label='Hang')
    ma_khach_hang__ten_khach_hang = CharFilter(label='Ten KH')
    class Meta:
        model = TheThanhVien
        fields = ['ma_the', 'hang', 'ma_khach_hang__ten_khach_hang']
        # fields = {
        #     'ma_the': ['icontains'],
        #     'hang': ['icontains'],
        #     'ma_khach_hang__ten_khach_hang': ['icontains'],
        # }
        #exclude = ['ma_khach_hang', 'tien_tich_luy', 'delete', 'tong_tien']
