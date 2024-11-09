BASE_DIR = server

venv:
	python3 -m venv env

install:
	sudo apt install build-essential gettext python3-dev libpq-dev libsqlite3-dev python3-django
	cd $(BASE_DIR) && mkdir -p static/
	cd $(BASE_DIR) && mkdir -p media/
	cd $(BASE_DIR) && mkdir -p locale/
	pip install -r requirements.txt

messages:
	cd $(BASE_DIR) && django-admin makemessages -l en  # for english translation;
	cd $(BASE_DIR) && django-admin makemessages -l fr  # for french translation;

build:
	django-admin compilemessages  # build i18n;

migrations:
	python3 server/manage.py makemigrations
	python3 server/manage.py migrate

sudo:
	python3 server/manage.py createsuperuser

run:
	hostname -I;
	python3 server/manage.py runserver 0.0.0.0:8000

test:
	pytest server;

shell:
	python3 server/manage.py shell

