from base import *
print("Running local Conf: {0}".format(BASE_DIR))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'taggersys',
        'USER': 'crojas',
        'PASSWORD': '123qweasd',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # During development only
