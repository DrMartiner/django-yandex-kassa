# -*- coding: utf-8 -*-

from app.models import Order
from .base_test import BaseTest
from django.core.urlresolvers import reverse


class TestPaymentForm(BaseTest):
    def setUp(self):
        self.url = reverse('home')

    def test_form_on_page(self):
        res = self.app.get(self.url)

        order = Order.objects.last()

        form_ctx = res.context['form']
        order_ctx = res.context['order']

        self.assertEquals(order_ctx, order, 'Order is not equals')
        self.assertEquals(order.payment.customer_number,
                          form_ctx.initial['customerNumber'],
                          'Payment form is not equals')
