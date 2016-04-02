from django.shortcuts import render
from django.http import HttpResponse
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
#PO
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf

from models import DataPoint

#  make users
#User.objects.create_user(username='petero',
#                                 email='peterostrovsky@ymail.com',
#                                 password='peter')
#User.objects.create_user(username='michaelk',
#                                 email='mike.kwan@hotmail.com',
#                                 password='michael')
#User.objects.create_user(username='eliasf',
#                                 email='ejfriedman7@gmail.com',
#                                 password='elias')
#User.objects.create_user(username='weijunq',
#                                 email='weijun.q@gmail.com',
#                                 password='weijun')
#User.objects.create_user(username='rosellen',
#                                 email='ri_ting@hotmail.com',
#                                 password='roselle')
#User.objects.create_user(username='jayg',
#                                 email='jgill.tftf@gmail.com',
#                                 password='jay')


# TODO: fix routing to make the login page the homepage
# serve login page
def login(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login.html', c)


def authview(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/dashboard/loggedin')
    else:
        return HttpResponseRedirect('/dashboard/invalidlogin')


def loggedin(request):
    return render_to_response('loggedin.html', {'full_name': request.user.username})


def invalidlogin(request):
    return render_to_response('invalidlogin.html')


def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')



# date  range //PO

# TODO: date  range //PO
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
    # return HttpResponse("Device ID %s " % watch_id)


# dynamic API for D3 graph
def live(request, watch_id):
    data = DataPoint.objects.filter(device_id=watch_id).values('device_id', 'accelTime', 'xAccel', 'yAccel', 'zAccel')
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