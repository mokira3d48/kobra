BASE_DIR = src
VENV_DIR = .venv
VENV_BIN = $(VENV_DIR)/bin
PYTHON3 = $(VENV_BIN)/python3

HOST = 0.0.0.0
PORT = 8000

install:
	sudo apt install build-essential gettext python3-dev python3-venv libpq-dev \
		libsqlite3-dev python3-django
	test -d $(VENV_DIR) || python3.10 -m venv $(VENV_DIR)
	cd $(BASE_DIR) && mkdir -p static/
	cd $(BASE_DIR) && mkdir -p media/
	cd $(BASE_DIR) && mkdir -p locale/
	cd $(BASE_DIR) && mkdir -p logs/
	$(PYTHON3) --version
	$(PYTHON3) -m pip install --upgrade pip
	$(PYTHON3) -m pip install -r requirements.txt

dev_install:
	$(PYTHON3) --version
	$(PYTHON3) -m pip install -e .

messages:
	cd $(BASE_DIR) && ../$(VENV_BIN)/django-admin makemessages -l en  # for english translation;
	cd $(BASE_DIR) && ../$(VENV_BIN)/django-admin makemessages -l fr  # for french translation;

build:
	$(VENV_BIN)/django-admin compilemessages  # build i18n;
	$(VENV_BIN)/manage collectstatic  # collect the static files;

migrations:
	$(PYTHON3) $(BASE_DIR)/manage.py makemigrations
	$(PYTHON3) $(BASE_DIR)/manage.py migrate

sudo:
	#.venv/bin/python3 $(BASE_DIR)/manage.py createsuperuser
	$(VENV_BIN)/manage createsuperuser

run:
	hostname -I
	#.venv/bin/python3 $(BASE_DIR)/manage.py runserver 0.0.0.0:8000
	$(VENV_BIN)/manage runserver $(HOST):$(PORT)

schema:
	$(PYTHON3) $(BASE_DIR)/manage.py spectacular --file schema.yml

test:
	#.venv/bin/pytest $(BASE_DIR)
	$(VENV_BIN)/pytest .

shell:
	#.venv/bin/python3 $(BASE_DIR)/manage.py shell
	$(VENV_BIN)/manage shell
