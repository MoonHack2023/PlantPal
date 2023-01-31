from audioop import minmax
from datetime import datetime
# from tkinter import Y
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.generic import ListView, CreateView, UpdateView
from .models import temp, humidity, co2, tvoc
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

def about1(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))


    context = {
        "qst": temp.objects.all(),
        "qsh": humidity.objects.all(),
        "qsco2": co2.objects.all(),
        "qstvoc": tvoc.objects.all(),
        "t": times
    } 
    print(context)

    return render(request, 'blog/chart.html', context)

def about2(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))


    context = {
        "qst": temp.objects.all(),
        "qsh": humidity.objects.all(),
        "qsco2": co2.objects.all(),
        "qstvoc": tvoc.objects.all(),
        "t": times
    } 

    print(context["qsco2"])

    return render(request, 'blog/chart.html', context)

def login(request):
    password = request.POST['psw']
    username = request.POST['uname']
    if username == 'ccl19' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
        return redirect('/plant')
    elif username == 'yscamy' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
        return redirect('/plant')
    elif username == 'hjj120' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
        return redirect('/plant')
    elif username == 'kelvin' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
        return redirect('/plant')
    else:
        return redirect('/')

def form(request):
    return redirect('/about')

def plant_select(request):
    delete = False
    # plantname = request.POST['plantname']
    # add = request.GET['add']
    d = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","r")
    
    lines = d.readlines()

    if 'plant_rem' in request.POST and len(lines) > 0:
        print("LINES IN HERE", lines)
        if len(lines) == 1:
            delete = True
        if request.POST['plant_rem'] == "HACK2":
            g = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w+")
            new = str(lines.pop(0))
            new = new.replace("\n", "")
            g.write(new)
        elif request.POST['plant_rem'] == "HACK1":
            g = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w+")
            new = str(lines.pop())
            new = new.replace("\n", "")
            g.write(new)
        g.close()
    
    print("lines",lines)
    if 'plant_type' in request.POST and len(lines)<2:
        print("INSIDE")
        if 'serialno' in request.POST and request.POST['serialno'] == "HACK1" and len(lines) > 0:
            print("SE1")
            f = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w+")
            f.write(str(request.POST['plant_type']) + "\n" + lines[0])
        elif 'serialno' in request.POST and request.POST['serialno'] == "HACK2" and len(lines) > 0:
            print("SE2")
            f = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w+")
            f.write(lines[0] + "\n" + str(request.POST['plant_type']))
        elif len(lines) == 0:
            print("EMP")
            f = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w+")
            f.write(str(request.POST['plant_type']))
        f.close()
    
    # print(plantname)
    
    # plant = ["Lavender", "Rose"]
    if delete:
        t = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","w")
        t.close()
    # else:
    t = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","r")
    lines = t.readlines()
    t.close()
    print(lines)
    plant = lines

    if len(plant) == 2:
        context = {
            "length": 2,
            "first": plant[0],
            "second": plant[1]
        }   
    elif len(plant) == 1:
        context = {
            "length": 1,
            "first": plant[0]
        }   
    else:
        context = {
            "length": 0
        } 
    

    return render(request, 'blog/plant.html', context)

def plant_setup(request):
    f = open("/Users/charmainelouie/Documents/Imperial/Year 3/EmbeddedSystems/PlantPal/PlantPalApp/blog/text_files/plants.txt","r")
    lines = f.readlines()
    f.close()

    if len(lines) == 2:
        alert = True
    else:
        alert = False
    
    

    context = {
        "alerts": alert
    }

    return render(request, 'blog/form.html', context)