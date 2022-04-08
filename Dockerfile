FROM python:3.10-slim-bullseye AS builder
RUN apt-get update && apt-get -y install libpq-dev build-essential
COPY requirements.txt /opt/tenttiarkisto/
WORKDIR /opt/tenttiarkisto
RUN python -m venv venv && venv/bin/python -m pip install -r requirements.txt

FROM python:3.10-slim-bullseye
RUN apt-get update && apt-get -y install libpq5
COPY --from=builder /opt/tenttiarkisto/venv /opt/tenttiarkisto/venv
COPY . /opt/tenttiarkisto
WORKDIR /opt/tenttiarkisto
RUN venv/bin/python manage.py collectstatic
# only set this after collectstatic, so it can copy files over without complaining about env vars
ENV DJANGO_SETTINGS_MODULE=tenttiarkisto.settings.production
CMD ["venv/bin/python", "-m", "gunicorn", "--bind=0.0.0.0:8000", "tenttiarkisto.wsgi"]
