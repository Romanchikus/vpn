!/bin/bash

set -e

python manage.py collectstatic --no-input

python ./manage.py migrate
pip list

gunicorn main.wsgi:application -w 4 --timeout 180 --bind 0.0.0.0:8000 --reload
