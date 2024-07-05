install:
	mkdir -p server/static/
	sudo apt install libpq-dev libsqlite3-dev python3-django
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
	pytest server
