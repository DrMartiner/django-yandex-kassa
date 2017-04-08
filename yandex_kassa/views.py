# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from . import conf
import json
import logging
from datetime import datetime
from xml.etree import ElementTree
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.generic import View
from django.views.generic import FormView
from django.views.generic import TemplateView

import six
from .forms import BaseMd5Form
from .forms import CheckOrderForm
from .forms import PaymentAvisoForm
from .models import Payment

logger = logging.getLogger('kassa')


class BaseFormView(FormView):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        post_data = json.dumps(self.request.POST, ensure_ascii=False)
        msg = 'URL="%s" POST="%s"' % (self.request.path, post_data)
        logger.debug(msg)

        return super(BaseFormView, self).dispatch(*args, **kwargs)

    def get_form_errors(self, form):
        errors = {}
        for name in form.fields:
            error = form.errors.get(name)
            if error:
                errors[name] = error[0]
        return errors

    def get_xml_element(self, **params):
        raise NotImplementedError()

    def get_xml(self, params):
        elem = self.get_xml_element(**params)
        return ElementTree.tostring(elem, 'unicode', 'xml')

    def get_response(self, content):
        content = '<?xml version="1.0" encoding="UTF-8"?>\n' + content
        return HttpResponse(content.encode('utf-8'),
                            content_type='application/xml')

    def form_invalid(self, form):
        errors = self.get_form_errors(form)

        msg = 'Ошибка при валидации формы проверки платежа '
        logger.info(msg, extra=dict(errors=errors))
        logger.debug(msg + str(errors))

        data = dict(code=200)  # Внутренняя ошибка магазина

        # Не совпал md5 hash
        if 'md5' in errors:
            data['code'] = 1

        # Платеж с таким номером не найден
        if 'orderNumber' in errors:
            data['code'] = 100

        # Устанавливаем статус в FAIL
        payment = form.get_payment()
        if payment:
            payment.status = Payment.STATUS.FAIL
            try:
                payment.save()
            except Exception as e:
                logger.warn('Ошибка при сохранение платеж', exc_info=True)

        content = self.get_xml(data)
        return self.get_response(content)

    def check_md5(self, cd):
        md5_hash = BaseMd5Form.make_md5(cd)
        return cd['md5'] == md5_hash


class CheckOrderView(BaseFormView):
    form_class = CheckOrderForm

    def form_valid(self, form):
        cd = form.cleaned_data

        order_num = cd['customerNumber']

        if not self.check_md5(cd):
            logger.warn('Ошибка при проверке MD5 платеж #%s' % order_num, exc_info=True)
            content = self.get_xml(dict(code=1))
            return self.get_response(content)

        payment = form.get_payment()
        if payment:
            payment.status = Payment.STATUS.PROCESSED
            payment.shop_amount = cd['shopSumAmount']
            payment.performed_datetime = datetime.now()
            payment.invoice_id = cd['invoiceId']

            try:
                payment.save()
            except Exception as e:
                logger.warn('Ошибка при сохранение платеж #%s' % order_num, exc_info=True)
                content = self.get_xml(dict(code=200))
                return self.get_response(content)
        else:
            logger.info('Платеж с номером #%s не найден' % order_num, exc_info=True)
            content = self.get_xml(dict(code=200))
            return self.get_response(content)

        payment.send_signals()

        data = dict(code=0, shopId=conf.SHOP_ID, invoiceId=cd['invoiceId'],
                    performedDatetime=payment.performed_datetime.isoformat())
        content = self.get_xml(data)
        logger.debug('Ответ CheckOrderView: "%s"' % content)
        return self.get_response(content)

    def get_xml_element(self, **params):
        params = {k: six.text_type(v) for k, v in params.items()}
        return ElementTree.Element('checkOrderResponse', attrib=params)


class PaymentAvisoView(BaseFormView):
    form_class = PaymentAvisoForm

    def form_valid(self, form):
        cd = form.cleaned_data

        order_num = cd['customerNumber']

        if not self.check_md5(cd):
            msg = 'Ошибка при проверке MD5 платеж #%s' % order_num
            logger.warn(msg, exc_info=True)
            content = self.get_xml(dict(code=1, message=msg))
            return self.get_response(content)

        payment = form.get_payment()
        payment.status = Payment.STATUS.SUCCESS
        if not payment.performed_datetime:
            payment.performed_datetime = datetime.now()

        try:
            payment.save()
            payment.send_signals()
            logger.info('Платеж #%s оплачен' % order_num)
        except Exception as e:
            msg = 'Ошибка при сохранение платеж #%s' % order_num
            logger.warn(msg, exc_info=True)
            content = self.get_xml(dict(code=200, message=msg))
            return self.get_response(content)

        # т.к. выжен порядок атрибутов :-(
        content = """<paymentAvisoResponse performedDatetime ="{0}" code="{1}" invoiceId="{2}" shopId="{3}" />
        """.format(
            payment.performed_datetime.isoformat(),
            0, payment.invoice_id, payment.shop_id
        )
        logger.debug('Ответ PaymentAvisoView: "%s"' % content)
        return self.get_response(content)

    def get_xml_element(self, **params):
        params = {k: six.text_type(v) for k, v in params.items()}
        return ElementTree.Element('paymentAvisoResponse', attrib=params)


class CancelOrderView(View):
    form_class = None


class SuccessPageView(TemplateView):
    template_name = 'yandex_kassa/success_page.html'


class FailPageView(TemplateView):
    template_name = 'yandex_kassa/fail_page.html'
