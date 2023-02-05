# import sqlite3
from blog.models import temp, humidity, co2, tvoc, light
from django.core.management.base import BaseCommand
import datetime
import time
### Run this executable to insert data into the database. 
## The database will change after running these series of commands.
# Allows for viewing of before and after.  

class Command(BaseCommand):
    help = 'import booms'
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #pass in every single element in sequence from this.
        # temp.objects.all().delete() 
        while True:
            f = open("blog/text_files/thsensor.txt", "r")
            # print(f.readline())
            # if (len(f.readline())> 0):
            th = f.readline()
            if len(th)> 0:
                splitth = th.split(",")
                tmp_var = temp(temp=splitth[0], device_id=splitth[-1])
                hum_var = humidity(humidity=splitth[1], device_id=splitth[-1])
                tv_var = tvoc(tvoc=splitth[2], device_id=splitth[-1])
                co_var = co2(co2=splitth[3], device_id=splitth[-1])
                light_var = light(red=splitth[4], orange=splitth[5], yellow=splitth[6], green=splitth[7], blue=splitth[8], violet=splitth[9], device_id=splitth[-1])
                # print("Before change map_info:",humidity.objects.all().values())
                tmp_var.save()
                hum_var.save()
                tv_var.save()
                co_var.save()
                light_var.save()
                time.sleep(5)
            # print("after change:",humidity.objects.all().values())



# class map_info(models.Model):
#     map_id = models.CharField(max_length=255,primary_key=True)
#     map_size = models.CharField(max_length=50)
#     date_time = models.DateTimeField(default=timezone.now)
