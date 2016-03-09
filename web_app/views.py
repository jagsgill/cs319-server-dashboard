from django.shortcuts import render
from django.http import HttpResponse
from models import Device


# Create your views here.

# home page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# analysis page
# TODO make query only get unique IDs
def get_device_ids(request):
    device_list = Device.objects.values('device_id').order_by('device_id')
    return render(request, 'dashboard.html', {'device_list': device_list})
