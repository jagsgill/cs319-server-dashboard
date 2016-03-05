from __future__ import unicode_literals

from django.db import models
from djangotoolbox.fields import EmbeddedModelField

# Create your models here.

class AccelerometerPayload(models.Model):
    x = models.FloatField(null=True)
    y = models.FloatField(null=True)
    z = models.FloatField(null=True)

class Location(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()

class WatchEvent(models.Model):
    timeStamp = DateTimeField()
    accelerometerPayload = ListField(EmbeddedModelField('AccelerometerPayload'))
    location = ListField(EmbeddedModelField('Location'))

class Device(models.Model):
    deviceId = DecimalField()
    watchEvents = ListField(EmbeddedModelField('WatchEvent'))