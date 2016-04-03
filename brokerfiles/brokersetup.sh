#!/bin/bash

# Note: to refresh the startup script used by Google Cloud, you need to
# completely remove the old one, then add new version as a new file/script.


#----------- Install Broker & Dependencies -----------#

# Note: Google Cloud's Debian (Wheezy) comes with OpenSSL already installed

sudo wget http://repo.mosquitto.org/debian/mosquitto-repo.gpg.key
sudo apt-key add mosquitto-repo.gpg.key

cd /etc/apt/sources.list.d/

sudo wget http://repo.mosquitto.org/debian/mosquitto-wheezy.list

sudo apt-get update --yes
sudo apt-get install mosquitto --yes

sudo kill $(pidof mosquitto) # kill the auto-started daemon so we can restart with new config files

sudo apt-get install mosquitto-clients --yes

#----------- Encryption Setup -----------#

# References:
#   http://mosquitto.org/man/mosquitto-tls-7.html
#   https://langui.sh/2009/01/18/openssl-self-signed-ca/
#   https://bowerstudios.com/node/1007
#   http://jpmens.net/2013/09/01/installing-mosquitto-on-a-raspberry-pi/
#   https://software.intel.com/en-us/blogs/2015/04/06/using-edison-securely-connect-iot-sensor-to-the-internet-with-mqtt

# Grab external-facing IP address
# Note: the instance needs at least Read Only permission to Google Cloud API
# Reference:
#   https://cloud.google.com/compute/docs/metadata

IP=$(gcloud compute instances list --format=text | grep '^networkInterfaces\[[0-9]\+\]\.accessConfigs\[[0-9]\+\]\.natIP:' | sed 's/^.* //g')

# We will use the IP address instead of a domain in the SSL certificates
# So we need to use a modified openssl.cnf file
# Reference:
#   https://bowerstudios.com/node/1007

PATH_BASE="/etc/mosquitto"
sudo chmod -R 777 '/etc/mosquitto'
PATH_SSL="$PATH_BASE/certs"

CNF='openssl.cnf'
sudo cp "/etc/ssl/$CNF" "$PATH_SSL/$CNF"
cd $PATH_SSL

# Add these lines according to the reference

sudo perl -i -p0e 's/# req_extensions/req_extensions/' $CNF

sudo perl -i -p0e "s/# Extensions to add to a certificate request\n\nbasicConstraints = CA:FALSE
keyUsage = nonRepudiation, digitalSignature, keyEncipherment/\nsubjectAltName = \@alt_names\n\n# Extensions to add to a certificate request\n\nbasicConstraints = CA:FALSE\nkeyUsage = nonRepudiation, digitalSignature, keyEncipherment\n\n[alt_names]\n\nIP.1 = $IP\n/s" $CNF

# Create CA, server, and client certificates/keys

PATH_CA="$PATH_BASE/ca_certificates"
cd $PATH_CA

CACERT=ca.crt
CAKEY=privkey.pem

# Generate Certificate Authority root certificate and private key
# No pass-phrases to keep it simple
sudo openssl req -newkey rsa:2048 -days 365 -x509 -nodes -out $CACERT -subj "/C=CA/ST=BritishColumbia/L=Vancouver/O=CA UBC CPSC/OU=CA TEAM TEN/CN=DEV CA"

cd $PATH_SSL

SERVERKEY=server.key
SERVERCSR=server.csr
SERVERCERT=server.pem

# Generate a server key and certificate signing request
sudo openssl req -newkey rsa:1024 -nodes -out $SERVERCSR -keyout $SERVERKEY -config "openssl.cnf" -new -subj "/C=CA/ST=BritishColumbia/L=Vancouver/O=UBC CPSC/OU=TEAM TEN/CN=$IP"

# Self-sign it with your CA key
sudo openssl x509 -req -in $SERVERCSR -CA $PATH_CA"/"$CACERT -CAkey $PATH_CA"/"$CAKEY -CAcreateserial -out $SERVERCERT -days 365 -extensions v3_req -extfile openssl.cnf

CLIENTKEY=client.key
CLIENTCSR=client.csr
CLIENTCERT=client.pem

# Generate a client key and certificate signing request
sudo openssl req -newkey rsa:1024 -nodes -out $CLIENTCSR -keyout $CLIENTKEY -new -subj "/C=CA/ST=BritishColumbia/L=Vancouver/O=UBC CPSC/OU=TEAM TEN/CN=client"

# Self-sign it with your CA key
sudo openssl x509 -req -in $CLIENTCSR -CA $PATH_CA"/"$CACERT -CAkey $PATH_CA"/"$CAKEY -CAcreateserial -out $CLIENTCERT -days 365 -extensions v3_req -extfile openssl.cnf


#----------- Mosquitto Broker Configuration -----------#

# Setup mosquitto.conf, access list file (user/pw), topic access list (define topics each users can read/write)
# Reference:
#   https://mosquitto.org/man/mosquitto-conf-5.html

CONF_FILE="mosquitto.conf"
PASSWD_FILE="mosquitto_accounts"
ACL_FILE="mosquitto_topic_access"
PID_FILE="mosquitto.pid"


PATH_CONF="$PATH_BASE/$CONF_FILE"           # /etc/mosquitto/mosquitto.conf
PATH_PASSWDFILE="$PATH_BASE/$PASSWD_FILE"   # password_file
PATH_ACL="$PATH_BASE/$ACL_FILE"             # acl_file
PATH_PID="$PATH_BASE/$PID_FILE"             # holds pid of running mosquitto process


sudo cp $PATH_CONF $PATH_CONF"_orig" # save original mosquitto.conf
sudo touch $PATH_CONF
sudo touch $PATH_PASSWDFILE # password_file
sudo touch $PATH_ACL # acl_file


read -d '' PASSWDFILE <<EOF
defaultwatch:vandricowatch
defaultserver:vandricoserver
broker:vandricobroker
EOF
echo "$PASSWDFILE" > $PATH_PASSWDFILE


read -d '' ACL <<EOF
# watches can read and write to any topic under the sensors topic
# it is a good idea for clients to publish under their client id
# e.g. sensors/<client id>/gps

user defaultwatch
topic readwrite sensors/#
topic readwrite \$SYS/broker/log/M/unsubscribe
topic read broker/#

# server can read from all topics
user defaultserver
topic read \$SYS/#
topic read #

# broker can read and write to any topic
user broker
topic readwrite #
EOF
echo "$ACL" > $PATH_ACL


CONF="
### General Options ###

# interval (seconds) to send updates to $SYS hierarchy
sys_interval 5

# location of the topic access file, disabled because using it stops logging to $SYS/# topics
# acl_file $PATH_ACL

# location of account user/pass file
password_file $PATH_PASSWDFILE

# only clients with valid user/pass will be allowed to connect
allow_anonymous false

# only few subscribers (server) so broker mem. usage will be low:
# when false the broker keeps track of who has received msgs -> consumes memory
allow_duplicate_messages false

# interval to save in-memory database to disk, in seconds
# treat interval as time (false), not as count of events (true)
autosave_on_changes false
autosave_interval 300

# log when client connect/disconnect
connection_messages true

# send log msgs to the topic \$SYS/broker/log/<severity>, <severity>=[D|E|W|N|I|M]
log_dest topic

# include timestamps in log messages
log_timestamp true

# log all msgs (except debug type which is never logged to log_dest topic)
log_type all

# no limit on number of QoS 1 or 2 msgs being transmitted simultaneously
# (if > 0, does broker reject excess msgs and client needs to retry??)
max_inflight_messages 0

# allow msgs up to the maximum payload size of 268435455 bytes
message_size_limit 0

# store subscription & msg data to disk according to autosave_interval
persistence true
persistence_file mosquitto.db
persistence_location $PATH_BASE/

# store the process id to a file when running in daemon mode
pid_file $PATH_PID


### Listeners ###

# unencrypted listener
listener 1883
protocol mqtt

# ssl listener
listener 8883
protocol mqtt

# allow unlimited client connections (limited by resource usage...)
max_connections -1

# do not replace client id of client with its username
use_username_as_clientid false

### Certificate-based SSL/TLS ###

# clients must provide a valid certificate to establish a connection
require_certificate true

# path to file containing trusted PEM encoded CA certificates
cafile $PATH_CA/$CACERT

# path to PEM encoded server certificate
certfile $PATH_SSL/$SERVERCERT

# path to PEM encoded keyfile
keyfile $PATH_SSL/$SERVERKEY
"
echo "$CONF" > $PATH_CONF


#----------- Encrypt Passwords -----------#

# Update the password file to use hashed passwords
# This is mandatory, otherwise broker startup fails due to incorrect password hashes

sudo mosquitto_passwd -U $PATH_PASSWDFILE

#----------- Start Broker -----------#

sudo mosquitto -c $PATH_CONF -d

#----------- Serve SSL certificates/keys to clients -----------#

# Serve the CA certificate and client cert/key files for clients
# Use --retain flag so we don't have to continually publish it

mosquitto_pub --retain -h $IP -p 1883 -t "broker/ssl/ca/cert" -u "broker" -P "vandricobroker" -f $PATH_CA"/"$CACERT
mosquitto_pub --retain -h $IP -p 1883 -t "broker/ssl/client/key" -u "broker" -P "vandricobroker" -f $PATH_SSL"/"$CLIENTKEY
mosquitto_pub --retain -h $IP -p 1883 -t "broker/ssl/client/cert" -u "broker" -P "vandricobroker" -f $PATH_SSL"/"$CLIENTCERT


# Also serve these files using public HTTP

KV=$(gcloud compute project-info describe | grep name) # gives 'name: <project name>'
PROJECTNAME=${KV#*: }   # use Bash parameter expansion to extract the project name

# create a Google Cloud Storage bucket with this unique name (if it doesn't already exist
BUCKET=gs://ssl-team10-cs319
sudo gsutil mb -p $PROJECTNAME          $BUCKET

# upload the files to the bucket
sudo gsutil cp $PATH_CA"/"$CACERT       $BUCKET
sudo gsutil cp $PATH_SSL"/"$CLIENTKEY   $BUCKET
sudo gsutil cp $PATH_SSL"/"$CLIENTCERT  $BUCKET

PATH_IP=$PATH_BASE
IPFILE=broker_ips.txt
PATH_IPFILE=$PATH_IP"/"$IPFILE
echo "$IP" > $PATH_IPFILE

sudo gsutil cp $PATH_IPFILE $BUCKET

# grant read access to anyone for all files in this bucket
sudo gsutil acl ch -u AllUsers:R $BUCKET/*

