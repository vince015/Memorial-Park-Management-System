#!/bin/bash
sudo systemctl stop nginx
sudo systemctl stop gunicorn

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

sudo systemctl start gunicorn
sudo systemctl start nginx
sudo systemctl enable nginx
