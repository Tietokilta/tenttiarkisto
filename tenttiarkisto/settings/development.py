import os
from django.core.exceptions import ImproperlyConfigured
from tenttiarkisto.settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'tenttiarkisto.db',      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'gkkqajw-l$iu85+p*4+bvsfhy)(!zxmh95g7h+-0k842zw!moe'

# Check that we don't accidentally run in development mode in a production environment
# https://docs.microsoft.com/en-us/azure/app-service/reference-app-settings
if os.environ.get('WEBSITE_SITE_NAME'):
  raise ImproperlyConfigured("cannot use development config in App Service")
