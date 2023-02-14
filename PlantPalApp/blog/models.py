from django.db import models
from django.utils import timezone

class User(models.Model):
    username = models.CharField(primary_key=True,max_length=50)
    password = models.CharField(max_length=100)

class Device(models.Model):
    device_no = models.CharField(primary_key=True, max_length=10)
    plant_name = models.CharField(max_length=50)
    score = models.FloatField(default=0)
    # login = models.CharField(max_length=50, default="ccl19")
    login = models.ForeignKey(User, on_delete=models.CASCADE, default="ccl19")
    temptip = models.CharField(max_length=50,default="ok")
    humtip = models.CharField(max_length=50,default="ok")
    co2tip = models.CharField(max_length=50,default="ok")
    tvoctip = models.CharField(max_length=50,default="ok")
    lighttip = models.CharField(max_length=50,default="ok")

class Plants(models.Model):
    plant_name = models.CharField(max_length=50, primary_key=True)
    optemp = models.CharField(max_length=50)
    ophumid = models.CharField(max_length=50)
    opco2 = models.CharField(max_length=50)
    optvoc = models.CharField(max_length=50)
    oplight = models.CharField(max_length=50)

class temp(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    temp = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class humidity(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    humidity = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class co2(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    co2 = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class tvoc(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    tvoc = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class light(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    red = models.FloatField(default=0)
    orange = models.FloatField(default=0)
    yellow = models.FloatField(default=0)
    green = models.FloatField(default=0)
    blue = models.FloatField(default=0)
    violet = models.FloatField(default=0)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class avglight(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    intensity = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class airVelocity(models.Model):
    time = models.DateTimeField(primary_key=True, auto_now=True)
    velocity = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class Leaderboard(models.Model):
    score = models.FloatField()
    user = models.CharField(primary_key=True, max_length=50)
    plant_name = models.CharField(max_length=50)