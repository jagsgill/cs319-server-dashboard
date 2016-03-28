from __future__ import unicode_literals

from django.db import models

# Create your models here.

class DataPoint(models.Model):
    device_id = models.CharField()
    accelTime = models.IntegerField()
    xAccel = models.FloatField()
    yAccel = models.FloatField()
    zAccel = models.FloatField()

    battery_level = models.FloatField(null=True)
    upload_rate = models.FloatField(null=True)

    gpsTime = models.IntegerField(null=True)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)

