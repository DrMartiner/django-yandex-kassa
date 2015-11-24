# -*- coding: utf-8 -*-

from django.dispatch import Signal

payment_process = Signal()
payment_completed = Signal()
payment_fail = Signal()
payment_success = Signal()
