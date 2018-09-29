#!/bin/bash
DIR="/usr/local/src/venv"

cd "/usr/local/src/"

if [ -d $DIR ]
then
    echo "Directory $DIR exists."
else
    echo "Error: Directory $DIR does not exists."
    python3.7 virtualenv venv
fi

# install requirements
source venv/bin/activate
pip3.7 install -r requirements.txt

python3.7 manage.py migrate

python3.7 manage.py createsu