from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, "management/home.html")

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