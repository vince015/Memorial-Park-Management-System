#!/bin/bash

cd /home/ubuntu/src

if [ ! -d "/home/ubuntu/src/venv" ]
then
   virtualenv venv --python=/usr/bin/python3.6
fi

# install requirements
source venv/bin/activate
pip  install -r requirements.txt

python manage.py collectstatic

python manage.py migrate

python manage.py createsu

python manage.py creategrp
