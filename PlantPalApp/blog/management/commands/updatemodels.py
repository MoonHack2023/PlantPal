# import sqlite3
from blog.models import temp, humidity, co2, tvoc, light, avglight, Leaderboard, User
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

        # Leaderboard(user="yscamy",score=51.37).save()
        # Leaderboard(user="hjj120",score=64.54).save()
        # Leaderboard(user="kelvin",score=32.15).save()
        # Leaderboard(user="lightning",score=51.82).save()
        # Leaderboard(user="neocandy",score=34.6).save()
        # Leaderboard(user="star-lord",score=52.4).save()
        # Leaderboard(user="milkyway",score=72.92).save()
        # Leaderboard(user="strawberry",score=55.2).save()
        # Leaderboard(user="venusnix",score=51.19).save()
        # Leaderboard(user="papillon",score=29.04).save()

        User(username='ccl19',password='8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4').save()
        User(username='hjj120',password='8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4').save()
        User(username='kelvin',password='8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4').save()
        User(username='yscamy',password='8f434346648f6b96df89dda901c5176b10a6d83961dd3c1ac88b59b2dc327aa4').save()



        # while True:
        #     f = open("blog/text_files/thsensor.txt", "r")
        #     # print(f.readline())
        #     # if (len(f.readline())> 0):
        #     th = f.readline()
        #     devices = ["HACK1", "HACK2","HACK3", "HACK4", "HACK5", "HACK6"]
        #     if len(th)> 0:
        #         splitth = th.split(",")
        #         for d in devices:
        #             # tmp_var = temp(temp=splitth[0], device_id=splitth[-1])
        #             # hum_var = humidity(humidity=splitth[1], device_id=splitth[-1])
        #             # tv_var = tvoc(tvoc=splitth[2], device_id=splitth[-1])
        #             # co_var = co2(co2=splitth[3], device_id=splitth[-1])
        #             # light_var = light(red=splitth[4], orange=splitth[5], yellow=splitth[6], green=splitth[7], blue=splitth[8], violet=splitth[9], device_id=splitth[-1])
        #             # avglight_var = avglight(intensity=splitth[10], device_id=splitth[-1])
        #             tmp_var = temp(temp=splitth[0], device_id=d)
        #             hum_var = humidity(humidity=splitth[1], device_id=d)
        #             tv_var = tvoc(tvoc=splitth[2], device_id=d)
        #             co_var = co2(co2=splitth[3], device_id=d)
        #             light_var = light(red=splitth[4], orange=splitth[5], yellow=splitth[6], green=splitth[7], blue=splitth[8], violet=splitth[9], device_id=d)
        #             avglight_var = avglight(intensity=splitth[10], device_id=d)
        #             # print("Before change map_info:",humidity.objects.all().values())
        #             tmp_var.save()
        #             hum_var.save()
        #             tv_var.save()
        #             co_var.save()
        #             light_var.save()
        #             avglight_var.save()
        #         time.sleep(5)
            # print("after change:",humidity.objects.all().values())



# class map_info(models.Model):
#     map_id = models.CharField(max_length=255,primary_key=True)
#     map_size = models.CharField(max_length=50)
#     date_time = models.DateTimeField(default=timezone.now)
