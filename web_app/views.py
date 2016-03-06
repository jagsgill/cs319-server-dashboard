from django.shortcuts import render
from django.http import HttpResponse
from models import Device

# Create your views here.

# home page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# analysis page
def getDevices(request):
    device_list = Device.objects
    return render(request, 'analysis.html', {'device_list': device_list})




