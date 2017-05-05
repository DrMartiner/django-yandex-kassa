# -*- coding: utf-8 -*-

from . import conf
from django.db import models
from django.conf import settings
from .signals import payment_process
from .signals import payment_completed
from .signals import payment_fail
from .utils import get_uuid


class Payment(models.Model):
    class STATUS:
        PROCESSED = 'processed'
        HOLD = 'hold'
        CANCEL = 'cancel'
        SUCCESS = 'success'
        FAIL = 'fail'

        CHOICES = (
            (PROCESSED, 'Processed'),
            (HOLD, 'Hold'),
            (CANCEL, 'Cancel'),
            (SUCCESS, 'Success'),
            (FAIL, 'Fail'),
        )

    class PAYMENT_TYPE:
        AB = 'AB'
        AC = 'AC'
        GP = 'GP'
        MA = 'MA'
        MC = 'MC'
        PB = 'PB'
        PC = 'PC'
        SB = 'SB'
        WM = 'WM'
        QW = 'QW'

        CHOICES = (
            (AB, u'Альфа-Клик'),
            (AC, u'Банковская карта'),
            (GP, u'Наличные через терминал'),
            (MA, u'MasterPass'),
            (MC, u'Мобильная коммерция'),
            (PB, u'Интернет-банк Промсвязьбанка'),
            (PC, u'Кошелек Яндекс.Денег'),
            (SB, u'Сбербанк Онлайн'),
            (WM, u'Кошелек WebMoney'),
            (QW, u'QiWi кошелёк'),
        )

    class CURRENCY:
        RUB = 643
        TEST = 10643

        CHOICES = (
            (RUB, u'Рубли'),
            (TEST, u'Тестовая валюта'),
        )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             verbose_name='Пользователь')
    customer_number = models.CharField('Номер заказа',
                                       unique=True, max_length=64,
                                       default=get_uuid)
    status = models.CharField('Результата', max_length=16,
                              choices=STATUS.CHOICES,
                              default=STATUS.PROCESSED)

    scid = models.PositiveIntegerField('Номер витрины',
                                       default=conf.SCID)
    shop_id = models.PositiveIntegerField('ID магазина',
                                          default=conf.SHOP_ID)
    payment_type = models.CharField('Способ платежа', max_length=2,
                                    default=PAYMENT_TYPE.PC,
                                    choices=PAYMENT_TYPE.CHOICES)
    invoice_id = models.CharField('Номер транзакции оператора',
                                  max_length=64, blank=True, null=True)
    order_amount = models.FloatField('Сумма заказа')
    shop_amount = models.DecimalField('Сумма полученная на р/с',
                                      max_digits=15,
                                      decimal_places=2,
                                      blank=True, null=True,
                                      help_text='За вычетом коммиссии')

    order_currency = models.PositiveIntegerField('Валюта платежа',
                                                 default=CURRENCY.RUB,
                                                 choices=CURRENCY.CHOICES)
    shop_currency = models.PositiveIntegerField('Валюта полученная на р/с',
                                                blank=True, null=True,
                                                default=CURRENCY.RUB,
                                                choices=CURRENCY.CHOICES)
    payer_code = models.CharField('Номер виртуального счета',
                                  max_length=33,
                                  blank=True, null=True)

    success_url = models.URLField('URL успешной оплаты',
                                  default=conf.SUCCESS_URL)
    fail_url = models.URLField('URL неуспешной оплаты', default=conf.FAIL_URL)

    cps_email = models.EmailField('Почта плательщика', blank=True, null=True)
    cps_phone = models.CharField('Телефон плательщика', max_length=15, blank=True, null=True)

    created = models.DateTimeField('Создан', auto_now_add=True)
    performed_datetime = models.DateTimeField('Обработан', blank=True, null=True)

    @property
    def is_payed(self):
        return self.status == self.STATUS.SUCCESS

    def send_signals(self):
        status = self.status
        if status == self.STATUS.PROCESSED:
            payment_process.send(sender=self.__class__, instance=self)
        if status == self.STATUS.SUCCESS:
            payment_completed.send(sender=self.__class__, instance=self)
        if status == self.STATUS.FAIL:
            payment_fail.send(sender=self.__class__, instance=self)

    class Meta:
        ordering = ('-created', )
        verbose_name = 'платеж'
        verbose_name_plural = 'Платежи'
