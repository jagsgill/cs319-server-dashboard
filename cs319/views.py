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
        return render_to_response('dashboard.html')
    else:
        return HttpResponseRedirect('/invalidlogin')

def loggedin(request):
    return render_to_response('loggedin.html', {'full_name': request.user.username})

def invalidlogin(request):
    return render_to_response('invalidlogin.html')

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')
