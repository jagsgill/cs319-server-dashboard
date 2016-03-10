
# -*- coding: utf-8 -*-
import sys
import os
import paho.mqtt.client as mqtt

# add paths so we can import some modules from our project and set the settings environment variable
sys.path.append('/vagrant/synced_data/cs319-server-webApp/cs319')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
sys.path.append("/vagrant/synced_data/cs319-server-webApp")
from web_app.models import DataPoint

# ------------------------------------------------------------------------------

# The callback for when the client receives a CONNACK response from the server.
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
def on_connect(client, userdata, rc):
    print ('Connected with result code ', str(rc))
    client.subscribe('hello/world') # TODO : use topics devices publish to
    return

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ('Topic: ', msg.topic, '\nMessage: ', str(msg.payload))

    messages = [x.strip() for x in str(msg.payload).split('$')]
    print("%%%%%" + str(messages))
    messages = messages[:-1]

    for msg in messages:
        arr = [x.strip() for x in msg.split(',')]
        print(arr)
        devId = str(arr[0])
        accelTime = str(arr[1])
        x = float(arr[2])
        print(str(msg[2]))
        print("***********" + str(arr[3]))
        print(str(arr[4]))
        y = float(arr[3])
        z = float(arr[4])
        gpsTime = int(arr[5])
        lat = float(arr[6])
        long = float(arr[7])

        datapoint = DataPoint(
        deviceId = devId,
        accelTime = accelTime,
        xAccel = x,
        yAccel = y,
        zAccel = z,
        gpsTime = gpsTime,
        lat = lat,
        long = long
        )

        datapoint.save()

    return

# MQTT connection
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# ----------------------------------------------------
# Choose same broker as devices

# Heroku broker:
#client.username_pw_set('ehcxlgcl', 'AQsUmTw6wYee')
#client.connect('m10.cloudmqtt.com', 10975, 60)

# Google Cloud broker:
client.connect('130.211.153.252', 1883, 60) # unencrypted
# client.connect('130.211.153.252', 8883, 60) # encrypted

# Other public testing brokers:
#client.connect('test.mosquitto.org', 1883, 60)
#client.connect('mq.thingmq.com', 1883, 60)
#client.connect('broker.mqttdashboard.com', 1883, 60)

# ----------------------------------------------------

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()