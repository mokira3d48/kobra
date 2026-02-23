FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DJANGO_SETTINGS_MODULE=core.settings
# ENV PYTHONPATH=/app

WORKDIR /app
# COPY requirements.txt /app
# COPY ./src /app
# COPY setup.py /app
# COPY README.md /app
# COPY manage.py /app
COPY . /app

RUN apt-get update && \
	apt-get install -y build-essential gettext python3-dev python3-venv libpq-dev libsqlite3-dev python3-django \
	&& rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && pip install -r requirements.txt

# RUN pip3 install git+https://github.com/mokira3d48/kobra.git@dev
RUN pip install -e .

# Create necessary directories including the one for logs
RUN mkdir -p src/static src/media src/locale src/logs # /usr/local/lib/python3.10/site-packages/logs

RUN python -m manage compilemessages

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000",  "core.wsgi:application", "--workers", "2", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "info"]
