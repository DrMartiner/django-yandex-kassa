# -*- coding: utf-8 -*-

from django.contrib import admin
from yandex_kassa.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('customer_number', 'is_payed_status', 'order_amount', 'payment_type',
                    'user', 'created', 'performed_datetime')
    list_filter = ('status', 'created', 'performed_datetime')
    search_fields = ('customer_number', 'invoice_id', 'payer_code')

    def is_payed_status(self, obj):
        return obj.is_payed

    is_payed_status.boolean = True
    is_payed_status.short_description = 'Оплачен'

    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Payment, PaymentAdmin)
