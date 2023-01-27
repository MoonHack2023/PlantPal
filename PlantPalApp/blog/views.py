from audioop import minmax
from datetime import datetime
# from tkinter import Y
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.generic import ListView, CreateView, UpdateView
from .models import temp, humidity
from django.db import connection
from django.db.models import Q
from django.db.models import Count
import os
from django.utils import timezone
import hashlib
import random
import datetime
import time


# def base(request):
#     return redirect('/home')

def home(request):
    context = { }
    return render(request, 'blog/base.html', context)

def about(request):
    # start_time = int(time.mktime(datetime.datetime(2012, 6, 1).timetuple()) * 1000)
    # nb_element = 100
    # xdata = range(nb_element)
    # xdata = map(lambda x: start_time + x * 1000000000, xdata)
    # ydata = [i + random.randint(1, 10) for i in range(nb_element)]
    # ydata2 = map(lambda x: x * 2, ydata)

    # tooltip_date = "%d %b %Y %H:%M:%S %p"
    # extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"},
    #                "date_format": tooltip_date}
    # chartdata = {'x': xdata,
    #              'name1': 'series 1', 'y1': ydata, 'extra1': extra_serie,
    #              'name2': 'series 2', 'y2': ydata2, 'extra2': extra_serie}
    # charttype = "lineChart"
    # data = {
    #     'charttype': charttype,
    #     'chartdata': chartdata
    # }
    # return render(request,'blog/linechart.html', data)
    
    
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))


    context = {
        "qst": temp.objects.all(),
        "qsh": humidity.objects.all(),
        "t": times
    } 

    # print(context["qs"].time)
    # context = super().get_context_data(**kwargs)
    # context["qs"] = temp.objects.all()

    # for d in context["qs"]:
    #     t
    print(context)

    return render(request, 'blog/chart.html', context)

def login(request):
    password = request.POST['psw']
    username = request.POST['uname']
    if username == 'ccl19' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '08c368c45b3e8d0c6ddc111a564f05dac269f1b1623ac4989b94b8d577d85d19':
        return redirect('/about')
    elif username == 'yscamy' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '65123d9463c1fa5535e014bfaf9c551481b1b4d227b587b917ca9f05c8edc778':
        return redirect('/about')
    elif username == 'hjj120' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8':
        return redirect('/about')
    elif username == 'kelvin' and hashlib.sha256(password.encode('utf-8')).hexdigest() == 'e45a1e24db27c12e9a60a38e56ade21c2f37e74adcd13959d01f898c27cae891':
        return redirect('/about')
    else:
        return redirect('/')

def form(request):
    return redirect('/about')

#takes distance and sends to back end 
#the file edited is distance.txt
def distance(request):
    context = {}

    return redirect ('/about', context)