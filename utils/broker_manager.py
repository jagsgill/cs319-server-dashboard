# -*- coding: utf-8 -*-

# SSL references:
# http://rockingdlabs.dunmire.org/exercises-experiments/ssl-client-certs-to-secure-mqtt
# https://jamielinux.com/docs/openssl-certificate-authority/sign-server-and-client-certificates.html

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
from web_app.models import DataPoint

# ----------- User Variables ----------- #

portEncrypted = 8883
portUnencrypted = 1883
timeout = 60

username = "defaultserver"
password = "vandricoserver"

clientId = "test_broker_manager"
sensorsTopic = "sensors/#"  # server subscribes to everything under

topicCACert = 'broker/ssl/ca/cert'
topicClientCert = 'broker/ssl/client/cert'
topicClientKey = 'broker/ssl/client/key'

sslDir = "/vagrant/synced_data/cs319-server-webApp/utils"

caCert = sslDir+"/ca.crt"
clientCert = sslDir+"/client.crt"
clientKey = sslDir+"/client.key"
sslFiles = [caCert, clientCert, clientKey]

tags = ['accel', 'gps', 'combined', 'batteryanduploadrate']


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


sslSetupClient = mqtt.Client()
sslSetupClient.on_connect = connect_for_ssl_setup
sslSetupClient.on_message = message_for_ssl_setup


# ----------- Setup subscriber ----------- #

# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.
def on_connect(client, userdata, rc):
    print(" *** Connected to broker: result code %s *** \n" % str(rc))
    client.subscribe(sensorsTopic)
    return


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print ('Topic: ', msg.topic, ' Message: ', str(msg.payload))

    # watches will send data to topics under sensors/<client id>
    # e.g. watch with id 999 sends gps data to sensors/999/gps
    # and we want to find the ending "tag" e.g. gps

    tag = ''
    for t in tags:  # tags is a constant defined in User Variables section
        if msg.topic.endswith(t):
            tag = t
            break

    # if tag is still empty, we cannot handle the msg type so warn and skip it
    if not tag:
        print(" **** WARNING: Unhandled Message Format **** ")
        print("       Topic: %s " % msg.topic)
        print("       Message: %s " % msg.payload)
        print("       Allowed types: %s " % tags)
        return

    handler = {
        # tag at end of topic : function to handle this type of msg
        "combined": combined_data_handler
    }.get(tag)

    # call the correct handler for the msg type
    handler(msg.payload)

    return

# ----------- Message Handlers ----------- #


def combined_data_handler(content):

    messages = [x.strip() for x in str(content.payload).split('$')]
    messages = messages[:-1]  # remove extra empty string at end

    for content in messages:
        arr = [x.strip() for x in content.split(',')]

        devId = str(arr[0])
        accelTime = str(arr[1])
        x = float(arr[2])
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






# ----------- Start subscriber ----------- #


client = mqtt.Client()
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


