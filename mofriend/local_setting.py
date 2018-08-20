import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = True

ALLOWED_HOSTS = ['localhost']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'sd',  # Or path to database file if using sqlite3.
    }
}