from os import environ
from django.core.exceptions import ImproperlyConfigured
from tenttiarkisto.settings import *

def get_env_var(name):
  value = environ.get(name)
  if not value:
    raise ImproperlyConfigured(f'Missing env variable: {name}')
  return value

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_var('DB_NAME'),
        'USER': get_env_var('DB_USER'),
        'PASSWORD': get_env_var('DB_PASSWORD'),
        'HOST': get_env_var('DB_HOST'),
        'PORT': environ.get('DB_PORT', ''),
        'OPTIONS': { 'sslmode': 'require' },
    }
}

DEFAULT_FILE_STORAGE = 'storages.backends.azure_storage.AzureStorage'

AZURE_ACCOUNT_NAME = get_env_var('EXAM_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = get_env_var('EXAM_ACCOUNT_KEY')
AZURE_CONTAINER = get_env_var('EXAM_CONTAINER')

SECRET_KEY = get_env_var('SECRET_KEY')

ALLOWED_HOSTS = get_env_var('ALLOWED_HOSTS').split(',')
