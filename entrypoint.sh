#!/bin/bash
cd /home/app/webapp
python manage.py collectstatic --settings=foodstockdjango.settings --noinput
python manage.py migrate --noinput
uwsgi --http "0.0.0.0:8000" --module foodstockdjango.wsgi:application --master --processes 4 --threads 2 --static-map /static=/static --static-map /media=/media