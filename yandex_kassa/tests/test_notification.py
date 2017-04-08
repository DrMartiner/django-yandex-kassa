# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from random import randint
from app.models import Order
from .base_test import BaseTest
from django.test import override_settings
from django.core.urlresolvers import reverse
from yandex_kassa.forms import CheckOrderForm
from yandex_kassa.models import Payment


@override_settings(YANDEX_KASSA_SHOP_ID=123)
class TestCheckOrder(BaseTest):
    def setUp(self):
        self.url = reverse('kassa_check_order')
        self.post_params = dict(
            requestDatetime='2011-05-04T20:38:00.000+04:00',
            action='checkOrder',
            shopId=123,
            shopArticleId=456,
            invoiceId=1234567,
            customerNumber=8123294469,
            orderCreatedDatetime='2011-05-04T20:38:00.000+04:00',
            orderSumAmount=87.10,
            orderSumCurrencyPaycash=643,
            orderSumBankPaycash=1001,
            shopSumAmount=86.23,
            shopSumCurrencyPaycash=643,
            shopSumBankPaycash=1001,
            paymentPayerCode='42007148320',
            paymentType='AC',
        )

    def test_check_order(self):
        params = self.post_params.copy()
        params['md5'] = CheckOrderForm.make_md5(params)

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        res = self.app.post(self.url, params=params)
        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.PROCESSED, 'Status is not set to "PROCESSED"')
        self.assertEquals(float(payment.shop_amount), params['shopSumAmount'], 'Shop amount was not changed')
        self.assertIsNotNone(payment.performed_datetime, 'Performed time was not set')

    def test_bad_form(self):
        params = self.post_params.copy()
        params['md5'] = CheckOrderForm.make_md5(params)

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        del params['orderSumAmount']  # Made form data as wrong
        res = self.app.post(self.url, params=params)

        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        body = b'<?xml version="1.0" encoding="UTF-8"?>\n<checkOrderResponse code="200" />'
        self.assertEqual(body, res.body, 'Body is not contains code="200"')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.FAIL, 'Status is not set to "FAIL"')
        self.assertIsNone(payment.shop_amount, 'Shop amount was set for wrond form data')
        self.assertIsNone(payment.performed_datetime, 'Performed time was set for wrond form data')

    def test_bad_md5(self):
        params = self.post_params.copy()
        params['md5'] = '4239da87569c3d29b7d712873561336c'  # Bas MD5 hash

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        res = self.app.post(self.url, params=params)

        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        body = b'<?xml version="1.0" encoding="UTF-8"?>\n<checkOrderResponse code="1" />'
        self.assertEqual(body, res.body, 'Body is not contains code="1"')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.PROCESSED, 'Status is not set to "FAIL"')
        self.assertIsNone(payment.shop_amount, 'Shop amount was set for wrond MD5 hash')
        self.assertIsNone(payment.performed_datetime, 'Performed time was set for wrond MD5 hash')


@override_settings(YANDEX_KASSA_SHOP_ID=123)
class PaymentAvisioTest(BaseTest):
    def setUp(self):
        self.url = reverse('kassa_payment_aviso')
        self.post_params = dict(
            requestDatetime='2011-05-04T20:38:00.000+04:00',
            action='paymentAviso',
            shopId=123,
            shopArticleId=456,
            invoiceId=1234567,
            customerNumber=8123294469,
            orderCreatedDatetime='2011-05-04T20:38:00.000+04:00',
            orderSumAmount=87.10,
            orderSumCurrencyPaycash=643,
            orderSumBankPaycash=1001,
            shopSumAmount=86.23,
            shopSumCurrencyPaycash=643,
            shopSumBankPaycash=1001,
            paymentDatetime='2011-05-04T20:38:10.000+04:00',
            paymentPayerCode=42007148320,
            paymentType='AC',
            cps_user_country_code='RU',
            MyField='Добавленное магазином поле',
        )

    def test_payment_aviso(self):
        params = self.post_params.copy()
        params['md5'] = CheckOrderForm.make_md5(params)

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        res = self.app.post(self.url, params=params)
        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.SUCCESS, 'Status is not set to "SUCCESS"')

    def test_bad_md5(self):
        params = self.post_params.copy()
        params['md5'] = '4239da87569c3d29b7d712873561336c'  # Bas MD5 hash

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        res = self.app.post(self.url, params=params)

        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        body = '<?xml version="1.0" encoding="UTF-8"?>\n<paymentAvisoResponse code="1" message="Ошибка при проверке MD5 платеж #8123294469" />'.encode('utf-8')
        self.assertEqual(body, res.body, 'Body is not contains code="1"')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.PROCESSED, 'Status is not set to "PROCESSED"')

    def test_bad_form(self):
        params = self.post_params.copy()
        params['md5'] = CheckOrderForm.make_md5(params)

        count = randint(1, 5)
        item = self.get_item()
        payment = Payment.objects.create(shop_id=params['shopId'],
                                         customer_number=params['customerNumber'],
                                         invoice_id=params['invoiceId'],
                                         order_amount=params['orderSumAmount'],
                                         order_currency=params['orderSumCurrencyPaycash'],
                                         payment_type=params['paymentType'])
        Order.objects.create(item=item, count=count,
                             amount=int(params['orderSumAmount']), payment=payment)

        del params['orderSumAmount']  # Made form data as wrong
        res = self.app.post(self.url, params=params)

        self.assertEquals(res.status_code, 200, 'HTTP code is not 200')

        body = b'<?xml version="1.0" encoding="UTF-8"?>\n<paymentAvisoResponse code="200" />'
        self.assertEqual(body, res.body, 'Body is not contains code="200"')

        payment = Payment.objects.get(pk=payment.pk)
        self.assertEquals(payment.status, Payment.STATUS.FAIL, 'Status is not set to "FAIL"')
        self.assertIsNone(payment.shop_amount, 'Shop amount was set for wrond form data')
        self.assertIsNone(payment.performed_datetime, 'Performed time was set for wrond form data')