import json
import time

from django.shortcuts import render
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from models import DataPoint

# date  range //PO
def get_device_by_time_range(request, start_time, end_time):
    device_list = DataPoint.objects.filter(accelTime__gte=start_time).filter(accelTime__lte=end_time)
    return render(request, 'dashboard.html', {'device_list': device_list}) # may need to be changed


# make query only get unique IDs //PO
# dashboard (device listing) page
def get_device_ids(request):
    if request.user.is_authenticated():
        distinct_device_list = Device.objects.all()
        online_device_list = ConnectedDevice.objects.all()
        offline_device_list = OfflineDevice.objects.all()

        distinct_device_count = TotalDeviceCount.objects.all()
        online_device_count = ConnectedDeviceCount.objects.all()
        offline_devices_count = OfflineDeviceCount.objects.all()
        return render(request, 'dashboard.html', {'distinct_device_list': distinct_device_list,
                                                  'online_device_list': online_device_list,
                                                  'offline_device_list': offline_device_list,
                                                  'distinct_device_count': distinct_device_count,
                                                  'online_device_count': online_device_count,
                                                  'offline_devices_count': offline_devices_count})
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('logout.html', c)


# dynamic analysis page for a device
def analyze_device(request, watch_id):
    if request.user.is_authenticated():
        device_data = DataPoint.objects.filter(device_id=watch_id)
        return render(request, 'analysis.html', {'device_data': device_data})
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('logout.html', c)


# dynamic API for D3 graph
def live(request, watch_id):
    seconds_partition = 4000
    data = DataPoint.objects.filter(device_id=watch_id, accelTime__gt=int(time.time())-seconds_partition).\
        values('device_id', 'accelTime', 'xAccel', 'yAccel', 'zAccel', 'battery_level')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')


# dynamic API for D3 graph
def live_with_date_range(request, watch_id):
    start_time = request.GET.get('start', '')
    end_time = request.GET.get('end', '')
    data = DataPoint.objects.filter(device_id=watch_id, accelTime__gte=int(start_time),
                                    accelTime__lte=int(end_time)).values('device_id', 'accelTime',
                                                                         'xAccel', 'yAccel', 'zAccel', 'battery_level')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')