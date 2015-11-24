# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='invoice_id',
            field=models.CharField(max_length=64, null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb7\xd0\xb0\xd0\xba\xd1\x86\xd0\xb8\xd0\xb8 \xd0\xbe\xd0\xbf\xd0\xb5\xd1\x80\xd0\xb0\xd1\x82\xd0\xbe\xd1\x80\xd0\xb0', blank=True),
        ),
    ]
