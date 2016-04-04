from django.test import TestCase
from web_app.models import DataPoint
from cs319.data_manager import DataManager

dm = DataManager()

class WebAppViewsTestCase(TestCase):
    def __init__(self):
        print ""

    def setup(self):
        DataPoint.objects.create(device_id = 1, accelTime = 4, xAccel = 5, yAccel = 6, zAccel = 7)
        DataPoint.objects.create(device_id = 2, accelTime = 4, xAccel = 5, yAccel = 6, zAccel = 7)

    def test_get_dist_dev_count(self):
        ct = dm.get_dist_dev_count()
        self.assertTrue(1 == ct)
        print("test_get_dist_dev_count passed")

    def test_get_dist_dev_list(self):
        ls = dm.get_dist_dev_list()
        self.assertTrue(len(ls) == 1)
        print("test_get_dist_dev_list passed")
        self.assertTrue(ls == [{'device_id': '1'}])
        print("test_get_dist_dev_list passed")


wa = WebAppViewsTestCase()
wa.test_get_dist_dev_count()
wa.test_get_dist_dev_list()