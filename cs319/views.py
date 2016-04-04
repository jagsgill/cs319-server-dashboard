
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout


def checklogin(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("dashboard/")
    else:
        c = {}
        c.update(csrf(request))
        return render_to_response('login.html', c)


def authview(request):
    u = request.POST.get('username', '')
    p = request.POST.get('password', '')
    user = authenticate(username=u, password=p)
    if user is not None:
        # the password verified for the user
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('dashboard/')
        else:
            return render_to_response('invalidlogin.html', {'full_name': request.user.username})
    else:
        return render_to_response('invalidlogin.html', {'full_name': request.user.username})


def invalidlogin(request):
    return render_to_response('invalidlogin.html')

def dologout(request):
    logout(request)
    c = {}
    c.update(csrf(request))
    return render_to_response('logout.html', c)