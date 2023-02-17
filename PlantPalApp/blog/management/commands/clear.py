from blog.models import temp, humidity, co2, tvoc, light, Device, avglight, airVelocity
from django.core.management.base import BaseCommand
import datetime
import time

class Command(BaseCommand):
    help = 'import booms'
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        #pass in every single element in sequence from this.
        temp.objects.all().delete() 
        humidity.objects.all().delete() 
        co2.objects.all().delete() 
        tvoc.objects.all().delete() 
        light.objects.all().delete()
        avglight.objects.all().delete()
        airVelocity.objects.all().delete()
        # Device.objects.all().delete()
            # print("after change:",humidity.objects.all().values())

