from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import render_to_response
from django.core.context_processors import csrf

from models import DataPoint
from cs319.data_manager import DataManager

dm = DataManager()

# date  range //PO
def get_device_by_time_range(request, start_time, end_time):
    device_list = DataPoint.objects.filter(accelTime__gte=start_time).filter(accelTime__lte=end_time)
    return render(request, 'dashboard.html', {'device_list': device_list}) # may need to be changed


# make query only get unique IDs //PO
# dashboard (device listing) page
def get_device_ids(request):
    if request.user.is_authenticated():
        return render(request, 'dashboard.html', {'device_list': dm.get_dist_dev_list(),
                                                  'distinct_device_count': dm.get_dist_dev_count()})
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
    data = DataPoint.objects.filter(device_id=watch_id).values('device_id', 'accelTime', 'xAccel', 'yAccel', 'zAccel', 'battery_level')
    json_str = json.dumps(list(data), cls=DjangoJSONEncoder)
    return HttpResponse(json_str, content_type='application/json; charset=utf8')