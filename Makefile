BASE_DIR = server

full-install:
	sudo apt install build-essential gettext python3-dev libpq-dev libsqlite3-dev python3-django
	python3 -m venv .venv
	cd $(BASE_DIR) && mkdir -p static/
	cd $(BASE_DIR) && mkdir -p media/
	cd $(BASE_DIR) && mkdir -p locale/
	.venv/bin/python3 --version
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -r requirements.txt

install:
	.venv/bin/python3 --version
	.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -r requirements.txt

messages:
	cd $(BASE_DIR) && .venv/bin/django-admin makemessages -l en  # for english translation;
	cd $(BASE_DIR) && .venv/bin/django-admin makemessages -l fr  # for french translation;

build:
	.venv/bin/django-admin compilemessages  # build i18n;

migrations:
	.venv/bin/python3 server/manage.py makemigrations
	.venv/bin/python3 server/manage.py migrate

sudo:
	.venv/bin/python3 server/manage.py createsuperuser

run:
	hostname -I;
	.venv/bin/python3 server/manage.py runserver 0.0.0.0:8000

test:
	.venv/bin/pytest server;

shell:
	.venv/bin/python3 server/manage.py shell

