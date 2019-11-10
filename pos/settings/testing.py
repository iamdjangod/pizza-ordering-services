from pos.settings.common import *

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.environ.get('DB_TEST_NAME'),
    }
}

MIGRATION_MODULES = {
    'customers': None,
    'orders': None,
    'pizzas': None
}
