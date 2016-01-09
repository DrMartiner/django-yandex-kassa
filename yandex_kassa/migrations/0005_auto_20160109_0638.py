# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '0004_auto_20151209_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='payment_type',
            field=models.CharField(default=b'pc', max_length=2, verbose_name=b'\xd0\xa1\xd0\xbf\xd0\xbe\xd1\x81\xd0\xbe\xd0\xb1 \xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xb6\xd0\xb0', choices=[(b'ab', '\u0410\u043b\u044c\u0444\u0430-\u041a\u043b\u0438\u043a'), (b'ac', '\u0411\u0430\u043d\u043a\u043e\u0432\u0441\u043a\u0430\u044f \u043a\u0430\u0440\u0442\u0430'), (b'gp', '\u041d\u0430\u043b\u0438\u0447\u043d\u044b\u0435 \u0447\u0435\u0440\u0435\u0437 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b'), (b'ma', 'MasterPass'), (b'mc', '\u041c\u043e\u0431\u0438\u043b\u044c\u043d\u0430\u044f \u043a\u043e\u043c\u043c\u0435\u0440\u0446\u0438\u044f'), (b'pb', '\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u0431\u0430\u043d\u043a \u041f\u0440\u043e\u043c\u0441\u0432\u044f\u0437\u044c\u0431\u0430\u043d\u043a\u0430'), (b'pc', '\u041a\u043e\u0448\u0435\u043b\u0435\u043a \u042f\u043d\u0434\u0435\u043a\u0441.\u0414\u0435\u043d\u0435\u0433'), (b'sb', '\u0421\u0431\u0435\u0440\u0431\u0430\u043d\u043a \u041e\u043d\u043b\u0430\u0439\u043d'), (b'wm', '\u041a\u043e\u0448\u0435\u043b\u0435\u043a WebMoney'), (b'qw', 'QiWi \u043a\u043e\u0448\u0435\u043b\u0451\u043a')]),
        ),
    ]
