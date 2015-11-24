# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0002_auto_20151111_1053'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('created',), 'verbose_name': '\u043f\u043b\u0430\u0442\u0435\u0436', 'verbose_name_plural': '\u041f\u043b\u0430\u0442\u0435\u0436\u0438'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='cps_email',
            field=models.EmailField(max_length=254, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c\xd1\x89\xd0\xb8\xd0\xba\xd0\xb0', blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\xa1\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbd'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='order_currency',
            field=models.PositiveIntegerField(default=643, verbose_name=b'\xd0\x92\xd0\xb0\xd0\xbb\xd1\x8e\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xb6\xd0\xb0', choices=[(643, '\u0420\u0443\u0431\u043b\u0438'), (10643, '\u0422\u0435\u0441\u0442\u043e\u0432\u0430\u044f \u0432\u0430\u043b\u044e\u0442\u0430')]),
        ),
        migrations.AlterField(
            model_name='payment',
            name='performed_datetime',
            field=models.DateTimeField(null=True, verbose_name=b'\xd0\x9e\xd0\xb1\xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd0\xb0\xd0\xbd', blank=True),
        ),
        migrations.AlterField(
            model_name='payment',
            name='scid',
            field=models.PositiveIntegerField(default=b'528277', verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb2\xd0\xb8\xd1\x82\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8b'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='shop_amount',
            field=models.DecimalField(decimal_places=2, max_digits=15, blank=True, help_text=b'\xd0\x97\xd0\xb0 \xd0\xb2\xd1\x8b\xd1\x87\xd0\xb5\xd1\x82\xd0\xbe\xd0\xbc \xd0\xba\xd0\xbe\xd0\xbc\xd0\xbc\xd0\xb8\xd1\x81\xd1\x81\xd0\xb8\xd0\xb8', null=True, verbose_name=b'\xd0\xa1\xd1\x83\xd0\xbc\xd0\xbc\xd0\xb0 \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x83\xd1\x87\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb0\xd1\x8f \xd0\xbd\xd0\xb0 \xd1\x80/\xd1\x81'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='shop_id',
            field=models.PositiveIntegerField(default=b'104674', verbose_name=b'ID \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd\xd0\xb0'),
        ),
    ]
