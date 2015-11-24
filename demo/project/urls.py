# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import admin
from django.conf.urls import include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from app import views

admin.autodiscover()

urlpatterns = [
    url(r'^$', views.HomeView.as_view(), name='home'),
    url(r'^order/(?P<pk>[\w-]+)/?$', views.OrderDetailView.as_view(), name='order_detail'),

    url(r'^kassa/', include('yandex_kassa.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

urlpatterns += staticfiles_urlpatterns(prefix=settings.STATIC_URL)
