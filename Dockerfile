FROM python:3.12-alpine AS builder
RUN apk add --no-cache libpq-dev build-base
COPY requirements.txt /opt/tenttiarkisto/
WORKDIR /opt/tenttiarkisto
RUN python -m venv venv && venv/bin/python -m pip install -r requirements.txt

FROM python:3.12-alpine
RUN apk add --no-cache libpq
COPY --from=builder /opt/tenttiarkisto/venv /opt/tenttiarkisto/venv
COPY . /opt/tenttiarkisto
WORKDIR /opt/tenttiarkisto
RUN venv/bin/python manage.py collectstatic
# only set this after collectstatic, so it can copy files over without complaining about env vars
ENV DJANGO_SETTINGS_MODULE=tenttiarkisto.settings.production
CMD ["venv/bin/python", "-m", "gunicorn", "--bind=0.0.0.0:8000", "--timeout", "600", "tenttiarkisto.wsgi"]
