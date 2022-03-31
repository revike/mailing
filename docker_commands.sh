#!/bin/sh

python3 mailing/manage.py migrate
python3 mailing/manage.py runserver 0.0.0.0:8080
