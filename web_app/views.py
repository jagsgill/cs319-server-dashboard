from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from models import DataPoint

#  make users
#User.objects.create_user(username='petero',
#                                 email='peterostrovsky@ymail.com',
#                                 password='peter')

# Create your views here.
# TODO: fix routing to make the login page the homepage


# date  range //PO
def get_device_by_time_range(request, start_time, end_time):
    device_list = DataPoint.objects.filter(accelTime__gte=start_time).filter(accelTime__lte=end_time)
    return render(request, 'dashboard.html', {'device_list': device_list}) # may need to be changed


# make query only get unique IDs //PO
# dashboard (device listing) page
def get_device_ids(request):
    device_list = DataPoint.objects.values('device_id').order_by('device_id')
    distinct_device_list = []
    for d in device_list:
        if d not in distinct_device_list:
            distinct_device_list.append(d)
    return render(request, 'dashboard.html', {'device_list': distinct_device_list})


# dynamic analysis page for a device
def analyze_device(request, watch_id):
    device_data = DataPoint.objects.filter(device_id=watch_id)
    return render(request, 'analysis.html', {'device_data': device_data})
    # return HttpResponse("Device ID %s " % watch_id)


# dynamic API for D3 graph
def live(request, watch_id):
    data = DataPoint.objects.filter(device_id=watch_id).values('device_id', 'accelTime', 'xAccel', 'yAccel', 'zAccel', 'battery_level')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')


# TODO: can we delete this method?
# demo page
# def demo(request):
#     desired_device = 'watch999'  # watch id
#     data = DataPoint.objects.filter(device_id = desired_device)
#     return render(request, 'analysis.html', {'data': data})
#     # desired_device = 'watch999'
#     # data = DataPoint.objects.filter(device_id = desired_device)
#     # return render(request, 'demo.html', {'data': data})
#     # accelTimes = DataPoint.objects.filter(lat__lt = 170).filter(lat__gt = 160)


# TODO: can we delete this method?
# parses demo data into correct format for demo javascript
# def parseDemoData(objectList):
#     parsed = []
#     for object in objectList:
#         point = "{{ x: {0}, time: {1} }}".format(object.xAccel, object.accelTime)
#         print(point)
#         parsed.append(point)
#     return parsed