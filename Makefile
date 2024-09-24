BASE_DIR = server

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
	./env/bin/python server/manage.py makemigrations
	./env/bin/python server/manage.py migrate

csudo:
	./env/bin/python server/manage.py createsuperuser

run:
	hostname -I;
	./env/bin/python server/manage.py runserver 0.0.0.0:8000

test:
	pytest server;
