from django.shortcuts import render
from django.http import HttpResponse
from .models import station_call
# Create your views here.

def index(request):
    all_station_items = station_call.objects.all()
    return render(request,'station.html',
        {'all_items': all_station_items})
