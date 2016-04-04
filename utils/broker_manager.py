# -*- coding: utf-8 -*-

# SSL references:
# http://rockingdlabs.dunmire.org/exercises-experiments/ssl-client-certs-to-secure-mqtt
# https://jamielinux.com/docs/openssl-certificate-authority/sign-server-and-client-certificates.html

# Important: as recently as Sept. 2015 http://stackoverflow.com/questions/32815429/detecting-duplicate-client-ids-in-mqtt
#            if 2 clients connect to Mosquitto broker using identical client ids, then they will fall into
#            a non-terminating disconnect-reconnect cycle. It is up to clients to have a unique client id !

import paho.mqtt.client as mqtt
import ssl
import sys
import os
import urllib2

# add paths so we can import some modules from our project and set the settings environment variable
sys.path.append('/vagrant/synced_data/cs319-server-webApp/cs319')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
sys.path.append("/vagrant/synced_data/cs319-server-webApp")
from web_app.models import *
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

# ----------- User Variables ----------- #

portEncrypted = 8883
portUnencrypted = 1883
timeout = 60

username = "defaultserver"
password = "vandricoserver"

clientId = "broker_manager"
clientsTopic = "client/watch/#"  # server subscribes to everything client's publish

# Note: make sure server has permission to read and/or write to all topics here:
topicCACert = 'broker/ssl/ca/cert'
topicClientCert = 'broker/ssl/client/cert'
topicClientKey = 'broker/ssl/client/key'
# topicBrokerConnectedDeviceCount = '$SYS/broker/clients/connected'  # for number of connected clients
# topicBrokerSubscribe = '$SYS/broker/log/M/subscribe'
# topicBrokerUnsubscribe = '$SYS/broker/log/M/unsubscribe'

sslDir = "/vagrant/synced_data/cs319-server-webApp/utils"

caCert = sslDir+"/ca.crt"
clientCert = sslDir+"/client.crt"
clientKey = sslDir+"/client.key"
sslFiles = [caCert, clientCert, clientKey]

sensor_data_tags = ['accel', 'gps', 'combined', 'batteryanduploadrate', 'status']


# ----------- Encrypted connection set-up ----------- #


# Get the Certificate Authority certificate from broker
# available with unsecured connection since it's a public cert.

def connect_for_ssl_setup(client, userdata, rc):
    print(" *** Starting SSL setup *** ")
    print(" Connected with result code %s " % str(rc))
    client.subscribe(topicCACert)
    client.subscribe(topicClientCert)
    client.subscribe(topicClientKey)
    print(" Subscribed to all SSL topics ")
    return


def message_for_ssl_setup(client, userdata, msg):
    print(" Received SSL setup file ")
    global sslFiles
    lastFile = False

    # if we have all the files, stop the ssl-setup client
    if len(sslFiles) == 1:
        lastFile = True

    path = {
        topicCACert:     caCert,
        topicClientCert: clientCert,
        topicClientKey:  clientKey
    }.get(msg.topic)

    sslFiles.remove(path)

    write_file(path, msg.payload)
    print(" Wrote file: %s " % path)

    if lastFile:
        print(" *** Finished SSL Setup *** \n")
        client.disconnect()

    return


def write_file(path, content):
    f = open(path, 'w')
    for line in content:
        f.write(line)
    f.close()
    return


sslSetupClient = mqtt.Client(clientId)
sslSetupClient.on_connect = connect_for_ssl_setup
sslSetupClient.on_message = message_for_ssl_setup


# ----------- Setup subscriber ----------- #

# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
def on_connect(client, userdata, rc):
    print(" *** Connected to broker: result code %s *** \n" % str(rc))
    # client.subscribe(topicBrokerConnectedDeviceCount)
    # client.subscribe(topicBrokerSubscribe)
    # client.subscribe(topicBrokerUnsubscribe)
    client.subscribe(clientsTopic)
    return


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # print ('Topic: ', msg.topic, ' Message: ', str(msg.payload))

    # watches will send data to topics under   client/watch/<client id>/combined
    # e.g. watch with id 999 sends gps data to client/watch/999/gps
    # and we want to find the ending "tag" e.g. gps and topic

    topic_parts = msg.topic.split('/')
    client_id = topic_parts[2]

    tag = ''
    for t in sensor_data_tags:  # tags is a constant defined in User Variables section
        if msg.topic.endswith(t):
            tag = t
            break

    # if tag is still empty, either it's an unknown msg type or a broker topic (.e.g $SYS/...)
    broker_tags = {
            # topicBrokerConnectedDeviceCount   : "clientcount",
            # topicBrokerSubscribe     : "clientsubscribe",
            # topicBrokerUnsubscribe   : "clientunsubscribe",
    }

    if not tag and msg.topic in broker_tags:
        tag = broker_tags.get(msg.topic)
    elif not tag:
        # otherwise output a warning on stdout
        print(" **** WARNING: Unhandled Message Format **** ")
        print("       Topic: %s " % msg.topic)
        print("       Message: %s " % msg.payload)
        print("       Allowed types: %s " % sensor_data_tags)
        return

    handler = {
        # tag at end of topic : function to handle this type of msg
        "combined"          : combined_data_handler,
        "clientcount"       : client_count_handler,
        "status"            : client_status_handler
        # "clientsubscribe"   : client_subscribe_to_broker_handler,
        # "clientunsubscribe" : client_unsubscribe_from_broker_handler
    }.get(tag)

    # call the correct handler for the msg type
    handler(client_id, msg.payload)

    return

# ----------- Message Handlers ----------- #


def combined_data_handler(client_id, content):
    print("Received data: %s" % str(content))

    data = content.split()  # split on newlines

    return

    # handler = None
    #
    # for msg in data:
    #     if 'Acceleration' in msg:
    #         print("Passing data to accel handler")
    #         handler = accel_msg_handler
    #         continue
    #     elif 'Location' in msg:
    #         print("Passing data to location handler")
    #         handler = location_msg_handler()
    #         continue
    #     elif 'Battery Level' in msg:
    #         print("Passing data to battery handler")
    #         handler = battery_msg_handler
    #         continue
    #     else:
    #         handler(msg)

    messages = [x for x in str(messages).split('$')]
    messages = messages[:-1]  # remove extra empty string at end

    print("accel msgs2: %s\n" % messages)

    for content in messages:
        arr = [x for x in content.split(',')]

        devId = str(arr[0])
        accelTime = str(arr[1])
        x = float(arr[2])
        y = float(arr[3])
        z = float(arr[4])
        gpsTime = int(arr[5])
        lat = float(arr[6])
        long = float(arr[7])

        datapoint = AccelPoint(
            deviceId = devId,
            accelTime = accelTime,
            xAccel = x,
            yAccel = y,
            zAccel = z,
            gpsTime = gpsTime,
            lat = lat,
            long = long
        )

        # datapoint.save()
    return


    return

# def accel_msg_handler(client_id, messages):
#
#     print("accel msgs1: %s\n" % messages)
#     messages = [x for x in str(messages).split('$')]
#     messages = messages[:-1]  # remove extra empty string at end
#
#     print("accel msgs2: %s\n" % messages)
#
#     for content in messages:
#         arr = [x for x in content.split(',')]
#
#         devId = str(arr[0])
#         accelTime = str(arr[1])
#         x = float(arr[2])
#         y = float(arr[3])
#         z = float(arr[4])
#         gpsTime = int(arr[5])
#         lat = float(arr[6])
#         long = float(arr[7])
#
#         datapoint = DataPoint(
#             deviceId = devId,
#             accelTime = accelTime,
#             xAccel = x,
#             yAccel = y,
#             zAccel = z,
#             gpsTime = gpsTime,
#             lat = lat,
#             long = long
#         )
#
#         # datapoint.save()
#     return
#
#
# def location_msg_handler(content):
#     # TODO
#     print("Location data: %s" % str(content))
#     return
#
#
# def battery_msg_handler(content):
#     print("Battery data: %s" % str(content))
#     return


def client_count_handler(status, id):
    try:
        if status == '1':
        # new or existing device connected
            print("Changing count, device connected: %s \n" % id)
            totalCountObj = TotalDeviceCount.objects.get()
            connectedCountObj = ConnectedDeviceCount.objects.get()
            setattr(totalCountObj, 'count', TotalDeviceCount.objects.count())
            setattr(connectedCountObj, 'count', ConnectedDevice.objects.count())
            totalCountObj.save()
            connectedCountObj.save()
        else:
            print("Changing count, device disconnected: %s \n" % id)
        # removing a device
            offlineCountObj = OfflineDevice.objects.get()
            setattr(offlineCountObj, 'count', OfflineDevice.objects.count())
            offlineCountObj.save()
    except ObjectDoesNotExist:
        # print("First run: no TotalDeviceCount and ConnectedDeviceCount objects in DB. Creating them...")
        TotalDeviceCount(count = Device.objects.count()).save()
        ConnectedDeviceCount(count = ConnectedDevice.objects.count()).save()
        OfflineDeviceCount(count = OfflineDevice.objects.count()).save()
    except MultipleObjectsReturned:
        # print("Warning: expected 1 ConnectedDeviceCount object in DB but found multiple... updating all")
        pass


    print("Count check: %s connected, %s disconnected, %s total devices" % (str(ConnectedDevice.objects.count()), str(OfflineDevice.objects.count()), str(Device.objects.count())))

    print("All devices:")
    for obj in Device.objects.all():
        print("    %s\n" % getattr(obj, '_id'))

    print("Connected devices:")
    for obj in ConnectedDevice.objects.all():
        print("    %s\n" % getattr(obj, '_id'))

    print("Offline devices:")
    for obj in OfflineDevice.objects.all():
        print("    %s\n" % getattr(obj, '_id'))

    return


def client_status_handler(client_id, content):
    # expect content to be a string of whitespace separated values
    # update connected device lists then update the connected device count
    data = content.split()
    if data[0] == '0':
        client_unsubscribe_from_broker_handler(data[1])
    else:
        client_subscribe_to_broker_handler(data[1])
    client_count_handler(data[0], data[1])
    return


def client_subscribe_to_broker_handler(id):
    # content should be unique client id
    print("Client subscribed:   %s" % id)
    try:
        Device(_id = id).save()
        ConnectedDevice(_id = id).save()
        OfflineDevice.objects.get(_id = id).delete()
    except Exception as e:
        print(str(e))
    return


def client_unsubscribe_from_broker_handler(id):
    # content should be unique client id
    # Clients must use a will: content=<client id> and will-topic=client/watch/<id>/status
    # in case they disconnect unexpectedly (e.g. loss of wifi)
    print("Client unsubscribed:   %s" % id)
    try:
        ConnectedDevice.objects.get(_id = id).delete()
        OfflineDevice(_id = id).save()
    except Exception as e:
        print(str(e))
    return


# ----------- Start subscriber ----------- #


client = mqtt.Client(clientId)
client.on_connect = on_connect
client.on_message = on_message


# Setup then connect to Google Cloud broker:
def start():
    global ENCRYPT

    set_broker_ip()

    if ENCRYPT:
        # run the setup client until all setup files are received
        sslSetupClient.username_pw_set(username, password)
        sslSetupClient.connect(brokerIP, portUnencrypted, timeout)
        sslSetupClient.loop_forever()

        # run the encrypted subscriber
        print(" Attempting encrypted connection to broker")
        client.username_pw_set(username, password)
        client.tls_set(caCert, clientCert, clientKey, ssl.CERT_REQUIRED)
        client.connect(brokerIP, portEncrypted, timeout)
        client.loop_forever() # run forever
    else:
        print(" Attempting unencrypted connection to broker ")
        client.username_pw_set(username, password)
        client.connect(brokerIP, portUnencrypted, timeout)
        client.loop_forever() # run forever
    return


def set_broker_ip():
    global brokerIP

    print(" Getting broker IP ... ")
    brokerIPlocation='https://storage.googleapis.com/ssl-team10-cs319/broker_ips.txt'
    IPdoc = urllib2.urlopen(brokerIPlocation)
    brokerIP = IPdoc.read().strip()
    print(" Found broker: %s" % brokerIP)
    return


if __name__ == '__main__':

    def usage():
        print("Usage: python %s [secure | insecure]" % sys.argv[0])
        sys.exit(64) # exit code 64: command line usage error
        return

    args = sys.argv[1:]
    global ENCRYPT

    if len(args) != 1:
        usage()
    elif args[0] == 'secure':
        ENCRYPT = True
    elif args[0] == 'insecure':
        ENCRYPT = False
    else:
        usage()

    print("\n *** Starting Up *** \n")
    start()


