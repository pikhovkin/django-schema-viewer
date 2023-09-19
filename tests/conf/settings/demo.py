from . import *


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DB_DIR = BASE_DIR.parent / 'data' / 'db'
DB_DIR.mkdir(parents=False, exist_ok=True)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DB_DIR / 'db.sqlite3',
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR.parent / 'data' / 'static'
STATIC_URL = '/static/'
