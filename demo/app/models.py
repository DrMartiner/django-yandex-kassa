# -*- coding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import truncatechars
from yandex_kassa.utils import get_uuid


class Item(models.Model):
    name = models.CharField('Наименование', max_length=32)
    price = models.PositiveIntegerField('Стоимость')

    def __unicode__(self):
        return truncatechars(self.name, 16)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Order(models.Model):
    uuid = models.CharField('ID заказа', max_length=64,
                            default=get_uuid, primary_key=True)
    item = models.ForeignKey('app.Item', verbose_name='Товар')
    count = models.PositiveIntegerField('Кол-во', default=1)
    payment = models.ForeignKey('yandex_kassa.Payment',
                                verbose_name='Платеж')
    amount = models.PositiveIntegerField('Сумма заказа')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
