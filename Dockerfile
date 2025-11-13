FROM python:3

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN mkdir /app

WORKDIR /app
COPY server /app/
COPY tests /app/
COPY requirements.txt /app/
COPY pyproject.toml /app/
COPY pytest.ini /app/
RUN ls -al .

RUN apt-get update && \
	apt-get install -y build-essential gettext python3-dev python3-venv libpq-dev libsqlite3-dev python3-django

RUN pip install --upgrade pip
RUN mkdir -p /app/server/static/
RUN mkdir -p /app/server/media/
RUN mkdir -p /app/server/locale/
RUN mkdir -p /app/server/logs/
RUN python --version
RUN pip install -r requirements.txt
RUN pip install .

RUN python -m manage compilemessages
RUN python -m manage makemigrations
RUN python -m manage migrate

