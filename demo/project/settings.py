# -*- coding: utf-8 -*-

import os
from os import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

settings_local_path = os.path.join(BASE_DIR, '../settings_local.py')
if settings_local_path:
    sys.path.insert(0, os.path.join(BASE_DIR, '..'))

try:
    from settings_local import *
except ImportError:
    pass

SECRET_KEY = '@f%mn40jz&wd$6!v(tt@67j-wlqy((h51jl$-oy_r0+$s-!fa7'

DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'app',
    'bootstrap3',
    'yandex_kassa',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True
USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = ''
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

YANDEX_KASSA_DEBUG = True
YANDEX_KASSA_SCID = 123
YANDEX_KASSA_SHOP_ID = 123
YANDEX_KASSA_SHOP_PASSWORD = 'password'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s] %(asctime)s - %(module)s: %(message)s [ERRORS = "%(errors)s"]'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'filters': {
        'kassa_errors': {
            '()': 'yandex_kassa.loggers.ErrorsFilter',
        }
    },
    'loggers': {
        'kassa': {
            'level': 'DEBUG',
            'propagate': False,
            'handlers': ['console', ],
            'filters': ['kassa_errors'],
        },
    },
}

try:
    from settings_local import *
except ImportError:
    pass
