from django.shortcuts import render
from django.http import HttpResponse
from models import Device
from models import Location

# Create your views here.

# home page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# analysis page
def getDevices(request):
    device_list = Location.objects.all()
    return render(request, 'dashboard.html', {'device_list': device_list})
