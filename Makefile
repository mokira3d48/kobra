BASE_DIR = server
VENV_DIR = .venv
VENV_BIN = $(VENV_DIR)/bin

HOST = 0.0.0.0
PORT = 8000

install:
	sudo apt install build-essential gettext python3-dev libpq-dev libsqlite3-dev python3-django
	test -d $(VENV_DIR) || python3 -m venv $(VENV_DIR)
	cd $(BASE_DIR) && mkdir -p static/
	cd $(BASE_DIR) && mkdir -p media/
	cd $(BASE_DIR) && mkdir -p locale/
	$(VENV_BIN)/python3 --version
	$(VENV_BIN)/python3 -m pip install --upgrade pip
	$(VENV_BIN)/python3 -m pip install -r requirements.txt

dev_install:
	.venv/bin/python3 --version
	#.venv/bin/python3 -m pip install --upgrade pip
	.venv/bin/python3 -m pip install -e .

messages:
	cd $(BASE_DIR) && ../$(VENV_BIN)/django-admin makemessages -l en  # for english translation;
	cd $(BASE_DIR) && ../$(VENV_BIN)/django-admin makemessages -l fr  # for french translation;

build:
	$(VENV_BIN)/django-admin compilemessages  # build i18n;

migrations:
	#.venv/bin/python3 $(BASE_DIR)/manage.py makemigrations
	#.venv/bin/python3 $(BASE_DIR)/manage.py migrate
	$(VENV_BIN)/manage makemigrations
	$(VENV_BIN)/manage migrate

sudo:
	#.venv/bin/python3 $(BASE_DIR)/manage.py createsuperuser
	$(VENV_BIN)/manage createsuperuser

run:
	hostname -I
	#.venv/bin/python3 $(BASE_DIR)/manage.py runserver 0.0.0.0:8000
	$(VENV_BIN)/manage runserver $(HOST):$(PORT)

test:
	#.venv/bin/pytest $(BASE_DIR)
	$(VENV_BIN)/pytest .

shell:
	#.venv/bin/python3 $(BASE_DIR)/manage.py shell
	$(VENV_BIN)/manage shell
