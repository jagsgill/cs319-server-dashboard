from __future__ import unicode_literals

from django.db import models
from djangotoolbox.fields import EmbeddedModelField
from djangotoolbox.fields import ListField

# Create your models here.

class AccelerometerPayload(models.Model):
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

class WatchEvent(models.Model):
    timeStamp = models.DateTimeField()
    accelerometer_payload = ListField(EmbeddedModelField('AccelerometerPayload'))
    location = ListField(EmbeddedModelField('Location'))

class Device(models.Model):
    _id = models.DecimalField(null=True)
    watch_events = ListField(EmbeddedModelField('WatchEvent'))