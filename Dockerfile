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

RUN python -m venv /env
ENV PATH="/env/bin/:$PATH"

COPY entrypoint.sh /app/entrypoint.sh

RUN apt-get update && \
	apt-get install -y build-essential gettext python3-dev python3-venv libpq-dev libsqlite3-dev python3-django

RUN python -m pip install --upgrade pip
RUN mkdir -p server/static/
RUN mkdir -p server/media/
RUN mkdir -p server/locale/
RUN mkdir -p server/logs/
RUN python --version
RUN python -m pip install -r requirements.txt
RUN python -m pip install -e .

RUN python -m manage compilemessages
RUN python -m manage collectstatic
# RUN python -m manage makemigrations
# RUN python -m manage migrate

