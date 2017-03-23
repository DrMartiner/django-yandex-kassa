# -*- coding: utf-8 -*-
import six

from . import conf
import logging
from hashlib import md5
from django import forms
from .models import Payment
from .utils import get_object_or_None

logger = logging.getLogger('kassa')

readonly_widget = forms.TextInput(
    attrs=dict(readonly='readonly')
)


class BaseShopIdForm(forms.Form):
    shopId = forms.IntegerField(initial=conf.SHOP_ID, widget=readonly_widget)

    def clean_shopId(self):
        shop_id = self.cleaned_data['shopId']
        if int(shop_id) != int(conf.SHOP_ID):
            raise forms.ValidationError(u'shopId не совпадает с YANDEX_KASSA_SHOPID')
        return shop_id


class BaseCustomerNumberForm(forms.Form):
    customerNumber = forms.CharField(label=' ID пользователя', min_length=1, max_length=64, widget=readonly_widget)

    def get_payment(self):
        customer_number = self.cleaned_data.get('customerNumber')
        return get_object_or_None(Payment, customer_number=customer_number)

    def clean_customerNumber(self):
        customer_number = self.cleaned_data['customerNumber']
        payment = get_object_or_None(Payment, customer_number=customer_number)
        if not payment:
            raise forms.ValidationError(
                u'Заказ с номером %s не найден' % six.text_type(customer_number)
            )
        return customer_number


class BaseOrderNumberForm(forms.Form):
    orderNumber = forms.CharField(label='Номер заказа', min_length=1, max_length=64, widget=readonly_widget)


class BaseMd5Form(forms.Form):
    md5 = forms.CharField(min_length=32, max_length=32, widget=readonly_widget)

    @staticmethod
    def make_md5(cd):
        """
        action;orderSumAmount;orderSumCurrencyPaycash;orderSumBankPaycash;shopId;invoiceId;customerNumber;shopPassword
        """
        cd = {k: six.text_type(v) for k, v in cd.items()}

        params = [cd['action'],
                  six.text_type(cd['orderSumAmount']),
                  six.text_type(cd['orderSumCurrencyPaycash']),
                  six.text_type(cd['orderSumBankPaycash']),
                  six.text_type(cd['shopId']),
                  six.text_type(cd['invoiceId']),
                  six.text_type(cd['customerNumber']),
                  conf.SHOP_PASSWORD]
        s = six.text_type(';'.join(params))
        return md5(s.encode('utf-8')).hexdigest().upper()


class BasePaymentTypeForm(forms.Form):
    paymentType = forms.CharField(label='Способ оплаты',
                                  widget=forms.Select(choices=Payment.PAYMENT_TYPE.CHOICES),
                                  min_length=2, max_length=2,
                                  initial=Payment.PAYMENT_TYPE.AC)

    def __init__(self, *args, **kwargs):
        super(BasePaymentTypeForm, self).__init__(*args, **kwargs)

        payment_types_choices = []
        for t in Payment.PAYMENT_TYPE.CHOICES:
            if t[0] in conf.PAYMENT_TYPES:
                payment_types_choices.append(t)
        self.fields['paymentType'].widget.choices = payment_types_choices


class BaseActionForm(forms.Form):
    class ACTION:
        CHECK = 'checkOrder'
        CPAYMENT = 'paymentAviso'

        CHOICES = (
            (CHECK, 'Проверка заказа'),
            (CPAYMENT, 'Уведомления о переводе'),
        )

    action = forms.CharField(max_length=16,
                             widget=forms.Select(choices=ACTION.CHOICES))


class BaseInvoiceId(forms.Form):
    invoiceId = forms.IntegerField(min_value=1)


class BaseOrderForm(forms.Form):
    orderSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    orderSumCurrencyPaycash = forms.IntegerField()
    orderSumBankPaycash = forms.IntegerField()
    shopSumAmount = forms.DecimalField(min_value=0, decimal_places=2)
    shopSumCurrencyPaycash = forms.IntegerField()
    shopArticleId = forms.IntegerField(required=False)


class PaymentForm(BaseShopIdForm, BasePaymentTypeForm,
                  BaseCustomerNumberForm, BaseOrderNumberForm):
    scid = forms.IntegerField(initial=conf.SCID, widget=readonly_widget)

    sum = forms.FloatField(label=u'Сумма заказа', min_value=0, widget=readonly_widget)

    cps_email = forms.EmailField(label=u'Почта', required=False)
    cps_phone = forms.CharField(label=u'Телефон', max_length=15, required=False)

    shopFailURL = forms.URLField(initial=conf.FAIL_URL, widget=forms.HiddenInput)
    shopSuccessURL = forms.URLField(initial=conf.SUCCESS_URL, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)

        self.fields['shopId'].widget.attrs['readonly'] = True

        if not conf.DEBUG:
            self.fields['scid'].widget = forms.HiddenInput()
            self.fields['shopId'].widget = forms.HiddenInput()
            self.fields['orderNumber'].widget = forms.HiddenInput()
            self.fields['customerNumber'].widget = forms.HiddenInput()

            for name in self.fields:
                if name not in self.get_display_field_names():
                    self.fields[name].widget = forms.HiddenInput()
        pass

    def clean_scid(self):
        scid = self.cleaned_data['scid']
        if scid != conf.SCID:
            raise forms.ValidationError(u'scid не совпадает с YANDEX_KASSA_SCID')
        return scid

    def get_display_field_names(self):
        return conf.DISPLAY_FIELDS

    @property
    def target(self):
        prefix = ''
        if conf.DEBUG:
            prefix = 'demo'
        return 'https://%smoney.yandex.ru/eshop.xml' % prefix


class CheckOrderForm(BaseShopIdForm, BasePaymentTypeForm,
                     BaseActionForm, BaseOrderForm,
                     BaseInvoiceId, BaseCustomerNumberForm, BaseMd5Form):
    pass


class PaymentAvisoForm(BaseActionForm, BaseShopIdForm,
                       BaseInvoiceId, BaseOrderForm,
                       BaseCustomerNumberForm, BasePaymentTypeForm, BaseMd5Form):
    pass
