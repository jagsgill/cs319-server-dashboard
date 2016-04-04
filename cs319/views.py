from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
import json
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required

def login(request):
    if request.user.is_authenticated():
        device_list = AccelPoint.objects.values('device_id').order_by('device_id')
        distinct_device_list = []
        distinct_device_count = 0
        for d in device_list:
            if d not in distinct_device_list:
                distinct_device_list.append(d)
                distinct_device_count += 1
        return render(request, 'dashboard.html', {'device_list': distinct_device_list,
                                              'distinct_device_count': distinct_device_count})

    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)

def authview(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = auth.authenticate(username=username,password=password)
    if user is not None:
        auth.login(request,user)
        device_list = AccelPoint.objects.values('device_id').order_by('device_id')
        distinct_device_list = []
        distinct_device_count = 0
        for d in device_list:
            if d not in distinct_device_list:
                distinct_device_list.append(d)
                distinct_device_count += 1
        return render(request, 'dashboard.html', {'device_list': distinct_device_list,
                                              'distinct_device_count': distinct_device_count})

    else:
        return render_to_response('invalidlogin.html', {'full_name': request.user.username})


def invalidlogin(request):
    return render_to_response('invalidlogin.html')

def logout(request):
    auth.logout(request)
    c = {}
    c.update(csrf(request))
    return render_to_response('logout.html', c)


