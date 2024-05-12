from os import environ
from django.core.exceptions import ImproperlyConfigured
from tenttiarkisto.settings import *


def get_env_var(name):
    value = environ.get(name)
    if not value:
        raise ImproperlyConfigured(f"Missing env variable: {name}")
    return value


DEBUG = False

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": get_env_var("DB_NAME"),
        "USER": get_env_var("DB_USER"),
        "PASSWORD": get_env_var("DB_PASSWORD"),
        "HOST": get_env_var("DB_HOST"),
        "PORT": environ.get("DB_PORT", ""),
        "OPTIONS": {"sslmode": "require"},
    }
}

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.azure_storage.AzureStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

AZURE_ACCOUNT_NAME = get_env_var("EXAM_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = get_env_var("EXAM_ACCOUNT_KEY")
AZURE_CONTAINER = get_env_var("EXAM_CONTAINER")

SECRET_KEY = get_env_var("SECRET_KEY")

ALLOWED_HOSTS = get_env_var("ALLOWED_HOSTS").split(",")

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "ERROR",
    },
    "loggers": {
        "django": {
            "level": "ERROR",
        },
        "django.security": {
            "level": "WARNING",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}
