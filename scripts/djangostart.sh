!/bin/bash

cd /home/ubuntu/src

if [ ! -d "/home/ubuntu/src" ]
then
    sudo virtualenv venv --python=/usr/local/lib/python3.7
fi

# install requirements
source venv/bin/activate
pip  install -r requirements.txt

python manage.py collectstatic

python manage.py migrate

python manage.py createsu

python manage.py creategrp