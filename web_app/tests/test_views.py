from django.test import TestCase
from web_app.models import DataPoint

class WebAppViewsTestCase(TestCase):
    def setup(self):
        DataPoint.objects.create(device_id = 2, accelTime = 4, xAccel = 5, yAccel = 6, zAccel = 7)
        DataPoint.objects.create(device_id = 2, accelTime = 4, xAccel = 5, yAccel = 6, zAccel = 7)





