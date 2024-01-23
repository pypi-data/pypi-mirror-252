#!/bin/bash
set -e

python django_nest/manage.py makemigrations
python django_nest/manage.py migrate
# python manage.py createsuperuser
python django_nest/manage.py runserver 0.0.0.0:8000
