install:
	sudo apt install build-essential python3-dev libpq-dev libsqlite3-dev python3-django
	mkdir -p server/static/
	mkdir -p server/media/
	pip install -r requirements.txt

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
