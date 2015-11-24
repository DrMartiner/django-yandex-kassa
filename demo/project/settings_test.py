# -*- coding: utf-8 -*-

from project.settings import *

DEBUG = False
YANDEX_KASSA_DEBUG = False
YANDEX_KASSA_SCID = 123
YANDEX_KASSA_SHOP_ID = 123
YANDEX_KASSA_SHOP_PASSWORD = 'password'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
