# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import yandex_kassa.utils
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('customer_number', models.CharField(default=yandex_kassa.utils.get_uuid, unique=True, max_length=64, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0')),
                ('status', models.CharField(default=b'processed', max_length=16, verbose_name=b'\xd0\xa0\xd0\xb5\xd0\xb7\xd1\x83\xd0\xbb\xd1\x8c\xd1\x82\xd0\xb0\xd1\x82\xd0\xb0', choices=[(b'processed', b'Processed'), (b'hold', b'Hold'), (b'cancel', b'Cancel'), (b'success', b'Success'), (b'fail', b'Fail')])),
                ('scid', models.PositiveIntegerField(default=528277, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb2\xd0\xb8\xd1\x82\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8b')),
                ('shop_id', models.PositiveIntegerField(default=104674, verbose_name=b'ID \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd\xd0\xb0')),
                ('payment_type', models.CharField(default=b'pc', max_length=2, verbose_name=b'\xd0\xa1\xd0\xbf\xd0\xbe\xd1\x81\xd0\xbe\xd0\xb1 \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xb6\xd0\xb0', choices=[(b'ab', '\u0410\u043b\u044c\u0444\u0430-\u041a\u043b\u0438\u043a'), (b'ac', '\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u0430\u0440\u0442\u0430'), (b'gp', '\u041d\u0430\u043b\u0438\u0447\u043d\u044b\u0435 \u0447\u0435\u0440\u0435\u0437 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b'), (b'ma', 'MasterPass'), (b'mc', '\u041c\u043e\u0431\u0438\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u044f'), (b'pb', '\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u0431\u0430\u043d\u043a \u041f\u0440\u043e\u043c\u0441\u0432\u044f\u0437\u044c\u0431\u0430\u043d\u043a\u0430'), (b'pc', '\u041a\u043e\u0448\u0435\u043b\u0435\u043a \u042f\u043d\u0434\u0435\u043a\u0441.\u0414\u0435\u043d\u0435\u0433'), (b'sb', '\u0421\u0431\u0435\u0440\u0431\u0430\u043d\u043a \u041e\u043d\u043b\u0430\u0439\u043d'), (b'wm', '\u041a\u043e\u0448\u0435\u043b\u0435\u043a WebMoney')])),
                ('invoice_id', models.PositiveIntegerField(null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb7\xd0\xb0\xd0\xba\xd1\x86\xd0\xb8\xd0\xb8 \xd0\xbe\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0', blank=True)),
                ('order_amount', models.FloatField(verbose_name=b'\xd0\xa1\xd1\x83\xd0\xbc\xd0\xbc\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0')),
                ('shop_amount', models.DecimalField(decimal_places=2, max_digits=15, blank=True, help_text=b'\xd0\x97\xd0\xb0 \xd0\xb2\xd1\x8b\xd1\x87\xd0\xb5\xd1\x82\xd0\xbe\xd0\xbc \xd0\xbf\xd1\x80\xd0\xbe\xd1\x86\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0 \xd0\xbe\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0', null=True, verbose_name=b'\xd0\xa1\xd1\x83\xd0\xbc\xd0\xbc\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0 \xd1\x80/\xd1\x81')),
                ('order_currency', models.PositiveIntegerField(default=643, verbose_name=b'\xd0\x92\xd0\xb0\xd0\xbb\xd1\x8e\xd1\x82\xd0\xb0', choices=[(643, '\u0420\u0443\u0431\u043b\u0438'), (10643, '\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0432\u0430\u043b\u044e\u0442\u0430')])),
                ('shop_currency', models.PositiveIntegerField(default=643, null=True, verbose_name=b'\xd0\x92\xd0\xb0\xd0\xbb\xd1\x8e\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0 \xd1\x80/\xd1\x81', blank=True, choices=[(643, '\u0420\u0443\u0431\u043b\u0438'), (10643, '\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0432\u0430\u043b\u044e\u0442\u0430')])),
                ('payer_code', models.CharField(max_length=33, null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb2\xd0\xb8\xd1\x80\xd1\x82\xd1\x83\xd0\xb0\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd1\x81\xd1\x87\xd0\xb5\xd1\x82\xd0\xb0', blank=True)),
                ('success_url', models.URLField(default=b'/kassa/success/', verbose_name=b'URL \xd1\x83\xd1\x81\xd0\xbf\xd0\xb5\xd1\x88\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd1\x8b')),
                ('fail_url', models.URLField(default=b'/kassa/fail/', verbose_name=b'URL \xd0\xbd\xd0\xb5\xd1\x83\xd1\x81\xd0\xbf\xd0\xb5\xd1\x88\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd1\x8b')),
                ('cps_email', models.EmailField(max_length=254, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd1\x8b \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd1\x89\xd0\xb8\xd0\xba\xd0\xb0', blank=True)),
                ('cps_phone', models.CharField(max_length=15, null=True, verbose_name=b'\xd0\xa2\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd1\x89\xd0\xb8\xd0\xba\xd0\xb0', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('performed_datetime', models.DateTimeField(null=True, verbose_name=b'\xd0\x92\xd1\x8b\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb7\xd0\xb0\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0', blank=True)),
                ('user', models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created',),
                'verbose_name': '\u041f\u043b\u0430\u0442\u0435\u0436',
                'verbose_name_plural': '\u041f\u043b\u0430\u0442\u0435\u0436\u0438',
            },
        ),
    ]
