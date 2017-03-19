# -*- coding: utf-8 -*-

from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^order-check/?$', views.CheckOrderView.as_view(), name='kassa_check_order'),
    url(r'^order-cancel/?$', views.CancelOrderView.as_view(), name='kassa_cancel_order'),
    url(r'^payment-aviso/?$', views.PaymentAvisoView.as_view(), name='kassa_payment_aviso'),

    url(r'^success/?$', views.SuccessPageView.as_view(), name='kassa_success'),
    url(r'^fail/?$', views.FailPageView.as_view(), name='kassa_fail'),
]
