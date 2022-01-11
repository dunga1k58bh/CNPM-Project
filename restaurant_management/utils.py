from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import  SuKien

HTMLCalendar.formatmonthname
class CalendarEvent(HTMLCalendar):
    def __init__(self, year=None, month = None):
        self.year = year
        self.month = month
        super(CalendarEvent, self).__init__()
        
    def formatday(self, day, events: SuKien):
        try:
            date = datetime(self.year, self.month, day)
            events_per_day = events.filter(ngay_bd__lte = date, ngay_kt__gte = date)
            d = ''

            for event in events_per_day:
                d+=f'<li>{event.ten_sk}</li>'
            if day != 0:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
            return '<td></td>'
        except: 
            return '<td></td>'

    
    
    def formatweek(self, theweek, events: SuKien):
        week = ''
        for d, weekday in theweek:
            week +=self.formatday(d, events)
        return f'<tr>{week}</tr>'
    
    def formatmonth(self, withyear = True):
        events = SuKien.objects.filter(ngay_bd__year__lte= self.year, ngay_bd__month__lte = self.month)
        cal_event = f'<table class="calendar">\n'
        cal_event += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal_event += f'{self.formatweekheader()} \n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal_event += f'{self.formatweek(week, events)}\n'
        cal_event += f'</table>'
        return cal_event
    
  
	