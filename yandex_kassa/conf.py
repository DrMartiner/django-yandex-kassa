# -*- coding: utf-8 -*-

import ast
import six
import logging
from django.conf import settings

logger = logging.getLogger('kassa')


DEBUG = getattr(settings, 'YANDEX_KASSA_DEBUG', False)
if isinstance(DEBUG, six.string_types[0]):
    DEBUG = ast.literal_eval(DEBUG)

SCID = getattr(settings, 'YANDEX_KASSA_SCID')
SHOP_ID = getattr(settings, 'YANDEX_KASSA_SHOP_ID')
SHOP_PASSWORD = getattr(settings, 'YANDEX_KASSA_SHOP_PASSWORD')

DISPLAY_FIELDS = getattr(settings, 'YANDEX_KASSA_DISPLAY_FIELDS',
                         ['paymentType', 'cps_email', 'cps_phone'])

CALLBACK_URL = getattr(settings, 'YANDEX_KASSA_CALLBACK_URL', '/kassa/callback/')
FAIL_URL = getattr(settings, 'YANDEX_KASSA_FAIL_URL', '/kassa/fail/')
SUCCESS_URL = getattr(settings, 'YANDEX_KASSA_SUCCESS_URL', '/kassa/success/')

PAYMENT_TYPES = getattr(settings, 'YANDEX_KASSA_PAYMENT_TYPE', None)

if PAYMENT_TYPES:
    msg = 'YANDEX_KASSA_PAYMENT_TYPE was deprecated. Rename it to YANDEX_KASSA_PAYMENT_TYPES'
    logger.warning(msg)
else:
    PAYMENT_TYPES = getattr(settings, 'YANDEX_KASSA_PAYMENT_TYPES', None)

if not PAYMENT_TYPES:
    PAYMENT_TYPES = ['AB', 'AC', 'GP', 'PB', 'PC', 'WM']
