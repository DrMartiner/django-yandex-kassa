# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0003_auto_20151116_1530'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ('-created',), 'verbose_name': '\u043f\u043b\u0430\u0442\u0435\u0436', 'verbose_name_plural': '\u041f\u043b\u0430\u0442\u0435\u0436\u0438'},
        ),
        migrations.AlterField(
            model_name='payment',
            name='scid',
            field=models.PositiveIntegerField(default=528277, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd0\xb2\xd0\xb8\xd1\x82\xd1\x80\xd0\xb8\xd0\xbd\xd1\x8b'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='shop_id',
            field=models.PositiveIntegerField(default=104674, verbose_name=b'ID \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd\xd0\xb0'),
        ),
    ]
