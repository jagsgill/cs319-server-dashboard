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
from web_app.models import DataPoint

class DataManager:


    def say_hello(self):
        return "Data Manager Init"

    def get_dist_dev_list(self):
        device_list = DataPoint.objects.values('device_id').order_by('device_id')
        distinct_device_list = []
        distinct_device_count = 0
        for d in device_list:
            if d not in distinct_device_list:
                distinct_device_list.append(d)
                distinct_device_count += 1
        return distinct_device_list

    def get_dist_dev_count(self):
        device_list = DataPoint.objects.values('device_id').order_by('device_id')
        distinct_device_list = []
        distinct_device_count = 0
        for d in device_list:
            if d not in distinct_device_list:
                distinct_device_list.append(d)
                distinct_device_count += 1
        return distinct_device_count
