# -*- coding: utf-8 -*-

from uuid import uuid4
from random import randint
from django_webtest import WebTest
from app.models import Item
from app.models import Order
from yandex_kassa.models import Payment


class BaseTest(WebTest):
    csrf_checks = False

    def get_item(self, **kwargs):
        params = dict(name=self.random,
                      price=randint(1, 9))
        params.update(**kwargs)

        return Item.objects.create(**params)

    def get_order(self, item=None, count=1, payment=None):
        if not item:
            item = self.get_item()

        amount = count * item.price

        if not payment:
            payment = self.get_payment(order_amount=amount)

        return Order.objects.create(item=item,
                                    count=count,
                                    payment=payment)

    def get_payment(self, user=None, **kwargs):
        params = dict(order_amount=randint(1, 9))
        params.update(**kwargs)

        return Payment.objects.create(user=user, **params)

    @property
    def random(self):
        return str(uuid4()).replace('', '-')[:8]
