from blog.models import temp, humidity
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
       
            # print("after change:",humidity.objects.all().values())

