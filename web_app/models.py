from __future__ import unicode_literals

from django.db import models
from djangotoolbox.fields import EmbeddedModelField
from djangotoolbox.fields import ListField

# from django_mongodb_engine import *

# Create your models here.

class AccelerometerPayload(models.Model):
    x = models.FloatField(null=False)
    y = models.FloatField(null=False)
    z = models.FloatField(null=False)

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

class WatchEvent(models.Model):
    timeStamp = models.DateTimeField()
    accelerometer_payload = ListField(EmbeddedModelField('AccelerometerPayload'))
    location = ListField(EmbeddedModelField('Location'))

class Device(models.Model):
    device_id = models.DecimalField(null=False)
    watch_events = ListField(EmbeddedModelField('WatchEvent'))

class DataPoint(models.Model):
    deviceId = models.CharField()

    accelTime = models.IntegerField()
    xAccel = models.FloatField();
    yAccel = models.FloatField();
    zAccel = models.FloatField();

    gpsTime = models.IntegerField();
    lat = models.FloatField()
    long = models.FloatField()

