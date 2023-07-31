#!/bin/bash
cd /home/app/webapp
python manage.py collectstatic --settings=badgering.settings --noinput
python manage.py migrate --noinput
uwsgi --http "0.0.0.0:8000" --module badgering.wsgi:application --master --processes 4 --threads 2 --static-map /static=/static --static-map /media=/media