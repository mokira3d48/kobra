install:
	pip install -r requirements.txt

migrations:
	./env/bin/python server/manage.py makemigrations
	./env/bin/python server/manage.py migrate

csudo:
	./env/bin/python server/manage.py createsuperuser

run:
	./env/bin/python server/manage.py runserver 0.0.0.0:8000

test:
	pytest server
