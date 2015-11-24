# -*- coding: utf-8 -*-

from random import randint
from django.http import Http404
from django.views.generic import DetailView
from django.views.generic import TemplateView
from yandex_kassa.forms import PaymentForm
from .models import Item
from .models import Order
from yandex_kassa.models import Payment


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        count = randint(1, 3)
        item = Item.objects.all().order_by('?').first()
        amount = count * item.price

        payment = Payment(order_amount=amount)
        payment.save()

        order = Order(item=item, count=count,
                      amount=amount, payment=payment)
        order.save()

        ctx = super(HomeView, self).get_context_data(**kwargs)
        ctx['order'] = order
        ctx['form'] = PaymentForm(initial=dict(orderNumber=order.uuid, sum=amount,
                                               customerNumber=payment.customer_number))
        return ctx


class OrderDetailView(DetailView):
    model = Order

    def get_object(self, queryset=None):
        try:
            return super(OrderDetailView, self).get_object(queryset)
        except UnicodeDecodeError:
            raise Http404
