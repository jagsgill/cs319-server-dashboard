from web_app.models import AccelerometerPayload
from web_app.models import Location
from web_app.models import WatchEvent
from web_app.models import Device
from random import *

accel = []
loc = []
event = []

for i in range(250):
   accel_val = AccelerometerPayload.objects.create(
        x = randint(10, 55),
        y = randint(10, 50),
        z = randint(10, 50)
    )
   accel.append(accel_val)

   loc_val = Location.objects.create(
        lat = uniform(-100, 100),
        lon = uniform(-100, 100)
    )
   loc.append(loc_val)


for i in range(10):
    event_val = WatchEvent.objects.create(
        timeStamp = "2016-2-" + str(randint(1, 28)) + " " + str(randint(0, 23)) + ":" + str(randint(0, 59)) + ":00",
        accelerometer_payload = accel,
        location = loc
    )
    event.append(event_val)


n = 1
for i in range(26):
    Device.objects.create(
        device_id = n,
        watch_events = event
    )
    if i % 4 == 0:
        n = n + 4