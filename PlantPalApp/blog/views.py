from audioop import minmax
from datetime import datetime
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.template import loader
from django.views.generic import ListView, CreateView, UpdateView
from .models import temp, humidity, co2, tvoc, Device, light, Plants, avglight, Leaderboard, User, airVelocity
# from django.db import connection
# from django.db.models import Q
# from django.db.models import Count
import os
from django.utils import timezone
import hashlib
import random
import datetime
import time
import openai
import re

no = "HACK1"
timeframe = "1 min"
timeskip = 1
user = ""
authenticate = 0

def plant_info(plant_name):
    openai.api_key = "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"

    model_engine = "text-davinci-003"
    
    prompt = "Give me the optimum temperature, humidity, carbon dioxide, tvoc and average intensity of light in watts per square meter for growing a "
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
        minValue = float(s[0])
        maxValue = float(s[1])
    else:
        minValue = float(value) - (float(value)*0.05)
        maxValue = float(value) + (float(value)*0.05)
    return minValue,maxValue


def checkOptimum(real, minValue, maxValue):
    count = 0
    tip = "ok"
    for i in real:
        if i >= minValue and i <= maxValue:
            count += 1
        elif i < minValue:
            tip = "Increase"
        elif i > maxValue:
            tip = "Decrease"
    if  len(real) == 0:
        score = -1
    else:
        score = count / len(real)
    return score, tip

def home(request):
    global authenticate

    if 'logout' in request.POST:
        print ("logout")
        authenticate = 0

    return render(request, 'blog/signup.html')

def about1(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))

    if 'serial_no' in request.POST:
        global no 
        no = request.POST['serial_no']

    if 'timeframe' in request.POST:
        global timeframe 
        global timeskip
        timeframe = request.POST['timeframe']

        if timeframe == "1 min":
            timeskip = 1
        elif timeframe == "3 mins":
            timeskip = 4
        elif timeframe == "30 mins":
            timeskip = 40
        elif timeframe == "1 hr":
            timeskip = 80
        elif timeframe == "2 hrs":
            timeskip = 160
        elif timeframe == "12 hrs":
            timeskip = 960
        elif timeframe == "1 day":
            timeskip = 1920

    print("SERIAL", no)
    print("timeskip", timeskip)
    length = len(temp.objects.filter(device_id=no).order_by('time')[::timeskip])
    
    if length > 9:
        temps = temp.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
        hums = humidity.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
        co2s = co2.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
        tvocs = tvoc.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
        velos = airVelocity.filter(device_id=no).order_by('time')[::timeskip][length-10:]
    else: 
        temps = temp.objects.filter(device_id=no).order_by('time')[::timeskip]
        hums = humidity.objects.filter(device_id=no).order_by('time')[::timeskip]
        co2s = co2.objects.filter(device_id=no).order_by('time')[::timeskip]
        tvocs = tvoc.objects.filter(device_id=no).order_by('time')[::timeskip]
        velos = airVelocity.filter(device_id=no).order_by('time')[::timeskip]


    context = {
        "qst": temps,
        "qsh": hums,
        "qsco2": co2s,
        "qstvoc": tvocs,
        "qsv": velos,
    } 

    global authenticate
    if authenticate == 1:
        return render(request, 'blog/chart.html', context)
    else:
        return redirect('/')

def about2(request):
    times =[]
    for d in temp.objects.all():
        times.append(str(d.time))

    global no
    global timeskip
    global timeframe

    length = len(temp.objects.filter(device_id=no).order_by('time')[::timeskip])

    if length > 9:
        lights = light.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
        avglights = avglight.objects.filter(device_id=no).order_by('time')[::timeskip][length-10:]
    else:
        lights = light.objects.filter(device_id=no).order_by('time')[::timeskip]
        avglights = avglight.objects.filter(device_id=no).order_by('time')[::timeskip]

    # print(avglights)

    context = {
        "qsl": lights,
        "qsal": avglights,
    } 
    
    global authenticate
    if authenticate == 1:
        return render(request, 'blog/chart2.html', context)
    else:
        return redirect('/')

def login(request):
    global user, authenticate
    
    if 'uname' in request.POST:
        password = request.POST['psw']
        password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        username = request.POST['uname']
        user = username
        print(password)
        # if user not in User.objects.values_list('username'):
        #     return redirect('/')
            
        if queryToValue(User.objects.filter(username=username).values('password'),'password') == password:
            authenticate = 1
            return redirect('/plant')
        else:
            return redirect('/')

    
    if 'newuname' in request.POST:
        newusername = request.POST['newuname']
        newpassword = request.POST['newpsw']
        newpassword = hashlib.sha256(newpassword.encode('utf-8')).hexdigest()
        User(username=newusername, password=newpassword).save()
        return redirect('/')
    
    # user = username
    print("user", user)
    # if username == 'ccl19' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
    #     authenticate = 1
    #     return redirect('/plant')
    # elif username == 'yscamy' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
    #     authenticate = 1
    #     return redirect('/plant')
    # elif username == 'hjj120' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
    #     authenticate = 1
    #     return redirect('/plant')
    # elif username == 'kelvin' and hashlib.sha256(password.encode('utf-8')).hexdigest() == '8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4':
    #     authenticate = 1
    #     return redirect('/plant')
    # elif 'logout' in request.POST:
    #     authenticate = 0
    #     return redirect('/')
    # else:
    #     return redirect('/')

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
        global user
        device_var = Device(device_no=serialno, plant_name=plant_type, login_id=user)
        print(plant_type)
        device_var.save()

    plant = Device.objects.filter(login_id=user).values_list('plant_name').order_by('device_no')
    device = Device.objects.filter(login_id=user).values_list('device_no').order_by('device_no')

    plant = queryToList(plant)

    device = queryToList(device)

    dp = list(zip(plant, device))
    
    context = {
        "devices": device,
        "plants": plant,
        "dps": dp,
        "timeframe": ["1 min", "3 mins", "30 mins", "1 hr", "2 hrs", "12 hrs", "1 day"],
        "user": user,
    }
    
    template = loader.get_template('blog/plant.html')
    
    global authenticate
    if authenticate == 1:
        return HttpResponse(template.render(context, request))
    else:
        return redirect('/')


def learn_more(request):
    plant = Device.objects.filter(login_id=user).values_list('plant_name').order_by('device_no')
    plant = queryToList(plant)
    # print(plant)

    # plant = ["Tomato","Rose","Rose"]
    # info = ["20°C, 60-70% humidity, 400-500ppm CO2, 0-10ppm TVOC, 400-700nm wavelength of light","20°C, 60-70% humidity, 400-500ppm CO2, 0-10ppm TVOC, 400-700nm wavelength of light"]
    # Plants.objects.all().delete()

    for p in plant:
        if Plants.objects.filter(plant_name=p).exists():
            print("OLD")
        else:
            print("NEW")
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

    print("here",Plants.objects.filter(plant_name__in=plant).values())

    context = {
        "pi": Plants.objects.filter(plant_name__in=plant).values(),
    }
    
    global authenticate
    if authenticate == 1:
        return render(request, 'blog/learnmore.html', context)
    else:
        return redirect('/')

def plant_setup(request):
    global authenticate
    if authenticate == 1:
        return render(request, 'blog/form.html')
    else:
        return redirect('/')

def score(request):
    global user
    print("score user", user)
    plant = Device.objects.filter(login_id=user).values_list('plant_name').order_by('device_no')
    plant = queryToList(plant)

    print(Device.objects.filter(login=user).values_list('device_no'))
    device = queryToList(Device.objects.filter(login_id=user).values_list('device_no').order_by('device_no'))
    print(device)

    num = [int(re.sub(r'[a-zA-Z]', '', d)) for d in device]
    if len(num) > 0:
        least = min(num)
        most = max(num)
    else:
        least = 0
        most = 0

    avg = [-100 for i in range(most+1)]

    for d in device:
        extemp = queryToList(temp.objects.filter(device_id=d).values_list("temp"))
        exhum = queryToList(humidity.objects.filter(device_id=d).values_list("humidity"))
        exco2 = queryToList(co2.objects.filter(device_id=d).values_list("co2"))
        extvoc = queryToList(tvoc.objects.filter(device_id=d).values_list("tvoc"))
        exlight = queryToList(avglight.objects.filter(device_id=d).values_list("intensity"))

        plant_name = list(Device.objects.filter(device_no=d).values('plant_name'))
        plant_name = queryToValue(plant_name, "plant_name")
        ideal_conditions = Plants.objects.filter(plant_name=plant_name).values()

        optemp = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('optemp')),"optemp")
        ophum = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('ophumid')),"ophumid")
        opco2 = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('opco2')),"opco2")
        optvoc = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('optvoc')),"optvoc")
        oplight = queryToValue(list(Plants.objects.filter(plant_name=plant_name).values('oplight')),"oplight")
        
        temp_range = findMaxMin(optemp)
        hum_range = findMaxMin(ophum)
        co2_range = findMaxMin(opco2)
        tvoc_range = findMaxMin(optvoc)
        avglight_range = findMaxMin(oplight)
        
        temp_score = checkOptimum(extemp, temp_range[0], temp_range[1])
        hum_score = checkOptimum(exhum, hum_range[0], hum_range[1])
        co2_score = checkOptimum(exco2, co2_range[0], co2_range[1])
        tvoc_score = checkOptimum(extvoc, tvoc_range[0], tvoc_range[1])
        avglight_score = checkOptimum(exlight, avglight_range[0], avglight_range[1])

        score = [temp_score[0], hum_score[0], co2_score[0], tvoc_score[0], avglight_score[0]]
    
        avg_score = (sum(score)/len(score))*100

        tips = [temp_score[1], hum_score[1], co2_score[1], tvoc_score[1], avglight_score[1]]

        avg_score = round(avg_score,2)
        device_entry = Device(device_no=d, plant_name=plant_name,score=avg_score,login_id=user,temptip=temp_score[1],humtip=hum_score[1],co2tip=co2_score[1],tvoctip=tvoc_score[1],lighttip=avglight_score[1]).save()
        devicenum = int(re.sub(r'[a-zA-Z]', '', d))
        avg[devicenum-least] = avg_score

    max_score = max(avg)
    # Leaderboard.objects.all().delete()
    if int(max_score) > 0:
        Leaderboard(user=user,score=max_score).save()

    f = open("score.txt", "w")
    f.write(str(avg)[1:-1])
    f.close()

    print(Device.objects.filter(login_id=user).all().order_by('device_no'))
    context ={
        "devices": Device.objects.filter(login_id=user).all().order_by('device_no')
    }

    global authenticate
    if authenticate == 1:
        return render(request, 'blog/score.html', context)
    else:
        return redirect('/')

def tips(request):
    context = {
        "devices": Device.objects.filter(login_id=user).all().order_by('device_no')
    }

    global authenticate
    if authenticate == 1:
        return render(request, 'blog/tips.html', context)
    else:
        return redirect('/')

def leaderboard(request):
    context = {
        "leaderboards": Leaderboard.objects.order_by('-score').all()
    }

    global authenticate
    if authenticate == 1:
        return render(request, 'blog/leaderboard.html', context)
    else:
        return redirect('/')
