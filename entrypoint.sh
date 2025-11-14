#!/bin/bash

set -e

source /env/bin/activate

# Run migrations
manage makemigrations
manage migrate

if [ "$1" == "gunicorn" ]; then
	gunicorn core.wsgi:application -b 0.0.0.0:8080
else
	manage runserver 0.0.0.0:8080
fi
