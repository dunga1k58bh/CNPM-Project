from django.forms import ModelForm, DateInput
from restaurant_management.models import MonAn, SuKien
from django.forms import Select


class EventForm(ModelForm):
  class Meta:
    model = SuKien
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'ngay_bd': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'ngay_kt': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    
    fields = ["ten_sk", "mo_ta", "ngay_bd", "ngay_kt", "ma_mon"]
    labels = {"ten_sk" : "Tên sự kiện","mo_ta": "Mô tả",
              "ngay_bd": "Thời gian bắt đầu", "ngay_kt": "Thời gian kết thúc", "ma_mon": "Món khuyến mãi"}
  
  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['ngay_bd'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['ngay_kt'].input_formats = ('%Y-%m-%dT%H:%M',)
    mon_an = MonAn.objects.filter(delete = 'NO')
    self.fields['ma_mon'].queryset = mon_an
