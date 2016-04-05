#!/bin/bash

# update repos, install git
sudo apt-get -qq  update --yes
sudo apt-get -qq install git --yes

# python development headers
sudo apt-get -qq install python-dev --yes
sudo apt-get -qq install libevent-dev --yes

# python-related packages
sudo apt-get -qq install python-pip --yes
yes | pip install virtualenv --upgrade --quiet
yes | pip install virtualenvwrapper --quiet

# install project-related packages:
# django, mongodb, paho-mqtt
yes | pip install paho-mqtt

yes | pip install git+git://github.com/django-nonrel/django@nonrel-1.5
yes | pip install git+git://github.com/django-nonrel/djangotoolbox
yes | pip install git+git://github.com/django-nonrel/mongodb-engine
yes | apt-get -qq install mongodb-server --yes

# edit the django runserver host url from 127.0.0.1 to 0.0.0.0 so we don't
# have to type 'python manage.py runserver 0.0.0.0:8000' to make it work
perl -pi -e 's/127.0.0.1/0.0.0.0/g' /usr/local/lib/python2.7/dist-packages/django/core/management/commands/runserver.py

# the project code is already available in the sync folder ./synced_data
# NOTE: ensure port forwarding is setup in the Vagrantfile for ports used
# at this point, you can ssh into the vm using 'vagrant ssh' and start using it



