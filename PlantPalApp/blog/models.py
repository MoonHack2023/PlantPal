from django.db import models
from django.utils import timezone


# Create your models here.
# class map_info(models.Model):
#     map_name = models.CharField(max_length=100)
#     map_id = models.IntegerField(primary_key=True)
#     map_size = models.CharField(max_length=50)
#     date_time = models.DateTimeField(default=timezone.now)
#     def _str_(self):
#         return self.map_id

# class Plant(models.Model):
#     plant_id = models.IntegerField(primary_key=True)
#     plant_name = models.CharField(max_length=50)

class Device(models.Model):
    device_no = models.CharField(primary_key=True, max_length=10)
    plant_name = models.CharField(max_length=50)
    score = models.FloatField(default=0)

class Plants(models.Model):
    plant_name = models.CharField(max_length=50, primary_key=True)
    optemp = models.CharField(max_length=50)
    ophumid = models.CharField(max_length=50)
    opco2 = models.CharField(max_length=50)
    optvoc = models.CharField(max_length=50)
    oplight = models.CharField(max_length=50)

class temp(models.Model):
    # plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, default=1)
    time = models.DateTimeField(primary_key=True, auto_now=True)
    temp = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class humidity(models.Model):
    # plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, default=1)
    time = models.DateTimeField(primary_key=True, auto_now=True)
    humidity = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class co2(models.Model):
    # plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, default=1)
    time = models.DateTimeField(primary_key=True, auto_now=True)
    co2 = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class tvoc(models.Model):
    # plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, default=1)
    time = models.DateTimeField(primary_key=True, auto_now=True)
    tvoc = models.FloatField()
    device = models.ForeignKey(Device, on_delete=models.CASCADE, default="")
    class Meta:
        ordering = ('time',)

class light(models.Model):
    # plant_id = models.ForeignKey(Plant, on_delete=models.CASCADE, default=1)
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


# class all_info(models.Model):
#     map_id = models.ForeignKey('map_info.map_id',on_delete=models.CASCADE,)
#     map_size = models.ForeignKey('map_info.map_size',on_delete=models.CASCADE,)
#     path = models.CharField(max_length=600)#designed to store the whole long path. 
#     tile_number = models.IntegerField()
#     tile_info = models.CharField(max_length=50)


    