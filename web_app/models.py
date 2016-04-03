from __future__ import unicode_literals

from django.db import models

# Create your models here.


class DataPoint(models.Model):
    # We do not use device_id as a primary key because the Device class is used
    # to store currently connected devices. When those are removed from the DB on
    # disconnect, the default behavior would be to remove all DataPoint documents
    # for the deleted device_id, which is not desired.
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


class TotalDeviceCount(models.Model):
    count = models.IntegerField()


class ConnectedDeviceCount(models.Model):
    count = models.IntegerField()


class OfflineDeviceCount(models.Model):
    count = models.IntegerField()


class Device(models.Model):
    _id = models.CharField(primary_key=True)


class ConnectedDevice(models.Model):
    _id = models.CharField(primary_key=True)


class OfflineDevice(models.Model):
    _id = models.CharField(primary_key=True)


