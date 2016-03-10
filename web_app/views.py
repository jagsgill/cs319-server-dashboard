from django.shortcuts import render
from django.http import HttpResponse
from web_app.models import Device
from web_app.models import Location
from models import DataPoint
import json
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.

# home page
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# analysis page
# TODO make query only get unique IDs
def get_device_ids(request):
    device_list = Device.objects.values('device_id').order_by('device_id')
    return render(request, 'dashboard.html', {'device_list': device_list})

# demo page
def demo(request):

    desired_device = 'watch999'  # watch id
    data = DataPoint.objects.filter(deviceId = desired_device)
    return render(request, 'analysis.html', { 'data' : data } )
    # desired_device = 'watch999'
    # data = DataPoint.objects.filter(deviceId = desired_device)
    # return render(request, 'demo.html', {'data': data})



    # accelTimes = DataPoint.objects.filter(lat__lt = 170).filter(lat__gt = 160)

def live(request):
    desired_device = 'watch999'  # watch id
    xAccel = DataPoint.objects.values('deviceId', 'accelTime', 'xAccel', 'yAccel', 'zAccel')
    str = json.dumps(list(xAccel), cls=DjangoJSONEncoder)
    print(str)
    return HttpResponse(str, content_type='application/json; charset=utf8')

    # data = DataPoint.objects.filter(deviceId = desired_device);
    # parsed = parseDemoData(data)
    # return render(request, 'demo.html', {'data': data})


# parses demo data into correct format for demo javascript
def parseDemoData(objectList):
    parsed = []
    for object in objectList:
        point = "{{ x: {0}, time: {1} }}".format(object.xAccel, object.accelTime)
        print(point)
        parsed.append(point)
    return parsed
