#!/bin/sh

# Docker's depends_on doesnt guarantee that a container will start
# before another, I created this small script to wait for the DB to be up and
# accepting connections

python db_wait.py
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
