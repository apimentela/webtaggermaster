import os
from unipath import Path
BASE_DIR = Path(__file__).ancestor(3)
SECRET_KEY = 'crem@a7bina*t3&81t-yj1p57e#+75xl@vwr07ze6ijx-4x^45'
DEBUG = True
ALLOWED_HOSTS = ['*',]
DJANGO_ADMIN_APPS = ['jet.dashboard', 'jet',]
DJANGO_APPS = [ 'django.contrib.admin',
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.messages',
                'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    'widget_tweaks',
    'django_extensions',
    'rest_framework',
	'session_security', 
	'tracking',	
]
LOCAL_APPS = [
    'apps.registro',
    'apps.usuarios',
    'apps.documentos',
]
INSTALLED_APPS = DJANGO_ADMIN_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
	'session_security.middleware.SessionSecurityMiddleware',
	'tracking.middleware.VisitorTrackingMiddleware',
	'apps.registro.middleware.UpdateSessionEnd',
]
ROOT_URLCONF = 'web_tagger.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.documentos.context_processors.context_processors_anotaciones',
            ],
        },
    },
]
WSGI_APPLICATION = 'web_tagger.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
AUTH_PASSWORD_VALIDATORS = [
]
LANGUAGE_CODE = 'es-MX'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = ''
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join('static'),)
MEDIA_URL  = '/media/'
os.path.join(BASE_DIR, 'media')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_true']
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logs/debug.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
        },
        'general': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'modelos': {
            'handlers': ['console', 'file'],
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
    }
}
DICCIONARIOS_PATH = os.path.join(BASE_DIR, 'docs/numeros/nums_para_editar_txt.dat')
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    )
}
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
LOGIN_REDIRECT_URL = '/'
SESSION_SECURITY_WARN_AFTER = 14 * 60
SESSION_SECURITY_EXPIRE_AFTER = 15 * 60
