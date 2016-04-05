import json
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from models import *

from django.contrib.auth.decorators import login_required


# date  range //PO
def get_device_by_time_range(request, start_time, end_time):
    device_list = AccelPoint.objects.filter(accelTime__gte=start_time).filter(accelTime__lte=end_time)
    return render(request, 'dashboard.html', {'device_list': device_list}) # may need to be changed


# make query only get unique IDs //PO
# dashboard (device listing) page
# @login_required(login_url="/login")
def build_dashboard(request):
    distinct_device_list = Device.objects.all().values('device_id')
    online_device_list = ConnectedDevice.objects.all().values('device_id')
    offline_device_list = OfflineDevice.objects.all().values('device_id')

    distinct_device_count = Device.objects.all().count()
    online_device_count = ConnectedDevice.objects.all().count()
    offline_devices_count = OfflineDevice.objects.all().count()
    return render(request, 'dashboard.html', {'distinct_device_list': distinct_device_list,
                                              'online_device_list': online_device_list,
                                              'offline_device_list': offline_device_list,
                                              'distinct_device_count': distinct_device_count,
                                              'online_device_count': online_device_count,
                                              'offline_devices_count': offline_devices_count})


# dynamic analysis page for a device
def analyze_device(request, watch_id):
    device_data = AccelPoint.objects.filter(device_id=watch_id)
    return render(request, 'analysis.html', {'device_data': device_data})


# dynamic API for D3 graph
def build_accel_api(request, watch_id):
    data = AccelPoint.objects.filter(device_id=watch_id).values('device_id', 'accelTime', 'xAccel', 'yAccel',
                                                                'zAccel').order_by('-accelTime')
    if len(data) > 100:
        data = data[0 : 100]
    else:
        pass
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')


# dynamic API for D3 graph
def build_accel_api_with_date(request, watch_id):
    start_time = request.GET.get('start', '0')
    end_time = request.GET.get('end', '0')
    data = AccelPoint.objects.filter(device_id=watch_id, accelTime__gte=int(start_time),
                                     accelTime__lte=int(end_time)).values('device_id', 'accelTime','xAccel', 'yAccel',
                                                                          'zAccel')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')


# dynamic API for D3 graph
def build_battery_api(request, watch_id):
    data = BatteryUploadRatePoint.objects.filter(device_id=watch_id).values('device_id', 'timestamp', 'battery_level',
                                                                            'upload_rate').order_by('-timestamp')
    if len(data) > 100:
        data = data[0 : 100]
    else:
        pass
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')


# dynamic API for D3 graph
def build_battery_api_with_date(request, watch_id):
    start_time = request.GET.get('start', '0')
    end_time = request.GET.get('end', '0')
    data = BatteryUploadRatePoint.objects.filter(device_id=watch_id, timestamp__gte=int(start_time),
                                                 timestamp__lte=int(end_time)).values('device_id', 'timestamp',
                                                                                      'battery_level', 'upload_rate')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')
