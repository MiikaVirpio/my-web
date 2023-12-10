from django.shortcuts import render

from miika.dash_apps.bda_va_1 import dash_launcher
from miika.dash_apps.bda_va_2 import dash_launcher
from miika.dash_apps.bda_va_4 import dash_launcher


def index(request):
    return render(request, 'index.html')

def dash_app_bda_va_1(request):
    return render(request, 'dash_apps/bda_va_1.html')

def dash_app_bda_va_2(request):
    return render(request, 'dash_apps/bda_va_2.html')

def dash_app_bda_va_4(request):
    return render(request, 'dash_apps/bda_va_4.html')
