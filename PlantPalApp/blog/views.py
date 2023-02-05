from audioop import minmax
from datetime import datetime
# from tkinter import Y
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.generic import ListView, CreateView, UpdateView
from .models import temp, humidity, co2, tvoc, Device, light, Plants
from django.db import connection
from django.db.models import Q
from django.db.models import Count
import os
from django.utils import timezone
import hashlib
import random
import datetime
import time
import openai
import re

import openai
import time

no = "HACK1"

def plant_info(plant_name):
    openai.api_key = "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"
    # insert your api key

    model_engine = "text-davinci-003"
    
    prompt = "Give me the optimum temperature, humidity, carbon dioxide, tvoc and wavlength of light conditions for growing a "
    # plant_name = input("Enter plant name: ")
    prompt = prompt + plant_name + " with units as a comma separated string"
    completion = openai.Completion.create(
        engine = model_engine,
        prompt = prompt,
        max_tokens = 1024,
        n=1,
        stop = None,
        temperature=0.5,)

    response = completion.choices[0].text
    response = response.strip()
    return(response)

def queryToList(query):
    queryList = []
    for q in query:
        queryList.append(q[0])
    return queryList

def queryToValue(query, key):
    return query[0][key]

def findMaxMin(value):
    s = value.split("-")
    if len(s) > 1:
        min = float(s[0])
        max = float(s[1])
    else:
        min = float(value) - (float(value)*0.1)
        max = float(value) + (float(value)*0.1)
    return min,max


def checkOptimum(real, min, max):
    count = 0
    for i in real:
        if i >= min and i <= max:
            count += 1
    if  len(real) == 0:
        score = 0.0
    else:
        score = count / len(real)
    return score

# def base(request):
#     return redirect('/home')

def home(request):
    context = { }
    return render(request, 'blog/base.html', context)

def about1(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))

    # no = "HACK1"
    if 'serial_no' in request.POST:
        global no 
        no = request.POST['serial_no']
    print(no)
    length = len(temp.objects.all())
    if length > 9:
        temps = temp.objects.filter(device_id=no).order_by('time')[length-10:]
        hums = humidity.objects.filter(device_id=no).order_by('time')[length-10:]
        co2s = co2.objects.filter(device_id=no).order_by('time')[length-10:]
        tvocs = tvoc.objects.filter(device_id=no).order_by('time')[length-10:]
        lights = light.objects.filter(device_id=no).order_by('time')[length-10:]
    else: 
        temps = temp.objects.filter(device_id=no).order_by('time')
        hums = humidity.objects.filter(device_id=no).order_by('time')
        co2s = co2.objects.filter(device_id=no).order_by('time')
        tvocs = tvoc.objects.filter(device_id=no).order_by('time')
        lights = light.objects.filter(device_id=no).order_by('time')

    context = {
        "qst": temps,
        "qsh": hums,
        "qsco2": co2s,
        "qstvoc": tvocs,
        "qsl": lights,
        "t": times
    } 
    # print(context)

    return render(request, 'blog/chart.html', context)

def about2(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))

    # if 'serial_no' in request.POST:
    #      no = request.POST['serial_no']
    global no
    length = len(light.objects.all())
    if length > 9:
        lights = light.objects.filter(device_id=no).order_by('time')[length-10:]
    else:
        lights = light.objects.filter(device_id=no).order_by('time')


    context = {
        "qst": temp.objects.all(),
        "qsh": humidity.objects.all(),
        "qsco2": co2.objects.all(),
        "qstvoc": tvoc.objects.all(),
        "qsl": lights,
        "t": times
    } 

    return render(request, 'blog/chart2.html', context)

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
    if 'plant_rem' in request.POST:
        plant_remove = request.POST['plant_rem']
        Device.objects.filter(device_no=plant_remove).delete()
    
    if 'plant_type' in request.POST and 'serialno' in request.POST:
        print("HERE")
        serialno = request.POST['serialno']
        plant_type = request.POST['plant_type']
        device_var = Device(device_no=serialno, plant_name=plant_type)
        print(plant_type)
        device_var.save()

    plant = Device.objects.values_list('plant_name').order_by('device_no')
    device = Device.objects.values_list('device_no').order_by('device_no')

    plant = queryToList(plant)

    device = queryToList(device)

    dp = list(zip(plant, device))
    
    context = {
        "devices": device,
        "plants": plant,
        "dps": dp
    }
    
    template = loader.get_template('blog/plant.html')
    # return render(request, 'blog/plant.html', context)
    return HttpResponse(template.render(context, request))

def learn_more(request):
    plant = Device.objects.values_list('plant_name').order_by('device_no')
    plant = queryToList(plant)
    # plant = ["Tomato","Rose","Rose"]
    # info = ["20°C, 60-70% humidity, 400-500ppm CO2, 0-10ppm TVOC, 400-700nm wavelength of light","20°C, 60-70% humidity, 400-500ppm CO2, 0-10ppm TVOC, 400-700nm wavelength of light"]
    # Plants.objects.all().delete()

    for p in plant:
        if Plants.objects.filter(plant_name=p).exists():
            print("OLD")
        else:
            print("NEW")
            # i = "25,60,400,0,400-700"
            i = plant_info(p)
            print(i)
            #find the info split here
            splitinfo = i.split(",")
            for j in range(len(splitinfo)):
                pattern = r'\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?'
                splitinfo[j] = re.findall(pattern, splitinfo[j])[0]
            print(splitinfo)
            plant_entry = Plants(plant_name=p, optemp=splitinfo[0], ophumid=splitinfo[1], opco2=splitinfo[2], optvoc=splitinfo[3], oplight=splitinfo[4])
            plant_entry.save()
    
    extemp = queryToList(temp.objects.values_list("temp"))
    exhum = queryToList(humidity.objects.values_list("humidity"))
    exco2 = queryToList(co2.objects.values_list("co2"))
    extvoc = queryToList(tvoc.objects.values_list("tvoc"))
    # exlight = queryToList(temp.objects.values_list(""))
    # print (checkOptimum(extemp, 10, 25))
    # print(extemp)


    device = queryToList(Device.objects.values_list('device_no').order_by('device_no'))

    for d in device:
        # print(queryToList(Device.objects.filter(plant_name=c).values_list("device_no")))
        extemp = queryToList(temp.objects.filter(device_id=d).values_list("temp"))
        exhum = queryToList(humidity.objects.filter(device_id=d).values_list("humidity"))
        exco2 = queryToList(co2.objects.filter(device_id=d).values_list("co2"))
        extvoc = queryToList(tvoc.objects.filter(device_id=d).values_list("tvoc"))
        plant_name = list(Device.objects.filter(device_no=d).values('plant_name'))
        plant_name = queryToValue(plant_name, "plant_name")
        ideal_conditions = Plants.objects.filter(plant_name=plant_name).values()
        # print(ideal_conditions)
        optemp = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('optemp')),"optemp")
        ophum = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('ophumid')),"ophumid")
        opco2 = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('opco2')),"opco2")
        optvoc = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('optvoc')),"optvoc")
        # ophum = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('ophumid')),"ophumid")
        
        temp_range = findMaxMin(optemp)
        hum_range = findMaxMin(ophum)
        co2_range = findMaxMin(opco2)
        tvoc_range = findMaxMin(optvoc)
        
        temp_score = checkOptimum(extemp, temp_range[0], temp_range[1])
        hum_score = checkOptimum(exhum, hum_range[0], hum_range[1])
        co2_score = checkOptimum(exco2, co2_range[0], co2_range[1])
        tvoc_score = checkOptimum(extvoc, tvoc_range[0], tvoc_range[1])
        print(temp_score)

        score = [temp_score, hum_score, co2_score, tvoc_score]
        avg_score = sum(score)/len(score)
        device_entry = Device(device_no=d, plant_name=plant_name,score=avg_score).save()
        print(avg_score)
        print(score)

    context = {
        "pi": Plants.objects.all(),
        "scores": score
    }

    return render(request, 'blog/learnmore.html', context)


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