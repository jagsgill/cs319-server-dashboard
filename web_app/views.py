from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder

from models import DataPoint

# date  range //PO
def get_device_by_time_range(request, start_time, end_time):
    device_list = DataPoint.objects.filter(accelTime__gte=start_time).filter(accelTime__lte=end_time)
    return render(request, 'dashboard.html', {'device_list': device_list}) # may need to be changed


# make query only get unique IDs //PO
# dashboard (device listing) page
def get_device_ids(request):
    device_list = DataPoint.objects.values('device_id').order_by('device_id')
    distinct_device_list = []
    distinct_device_count = 0
    for d in device_list:
        if d not in distinct_device_list:
            distinct_device_list.append(d)
            distinct_device_count += 1
    return render(request, 'dashboard.html', {'device_list': distinct_device_list,
                                              'distinct_device_count': distinct_device_count})


# dynamic analysis page for a device
def analyze_device(request, watch_id):
    device_data = DataPoint.objects.filter(device_id=watch_id)
    return render(request, 'analysis.html', {'device_data': device_data})


# dynamic API for D3 graph
def live(request, watch_id):
    data = DataPoint.objects.filter(device_id=watch_id).values('device_id', 'accelTime', 'xAccel', 'yAccel', 'zAccel', 'battery_level')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')