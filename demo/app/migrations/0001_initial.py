# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import migrations, models
import yandex_kassa.utils


def create_items(apps, schema_editor):
    Item = apps.get_model('app', 'Item')

    Item.objects.bulk_create([
        Item(name='HTC Desire', price=5),
        Item(name='iPhone 4', price=10),
        Item(name='iPhone 5', price=15),
        Item(name='iPhone 6', price=20),
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('yandex_kassa', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb8\xd0\xbc\xd0\xb5\xd0\xbd\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5')),
                ('price', models.PositiveIntegerField(verbose_name=b'\xd0\xa1\xd1\x82\xd0\xbe\xd0\xb8\xd0\xbc\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c')),
            ],
            options={
                'verbose_name': '\u0422\u043e\u0432\u0430\u0440',
                'verbose_name_plural': '\u0422\u043e\u0432\u0430\u0440\u044b',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('uuid', models.CharField(default=yandex_kassa.utils.get_uuid, max_length=64, serialize=False, verbose_name=b'ID \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0', primary_key=True)),
                ('count', models.PositiveIntegerField(default=1, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xbb-\xd0\xb2\xd0\xbe')),
                ('amount', models.PositiveIntegerField(verbose_name=b'\xd0\xa1\xd1\x83\xd0\xbc\xd0\xbc\xd0\xb0 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0')),
                ('item', models.ForeignKey(verbose_name=b'\xd0\xa2\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x80', to='app.Item')),
                ('payment', models.ForeignKey(verbose_name=b'\xd0\x9f\xd0\xbb\xd0\xb0\xd1\x82\xd0\xb5\xd0\xb6', to='yandex_kassa.Payment')),
            ],
            options={
                'verbose_name': '\u0417\u0430\u043a\u0430\u0437',
                'verbose_name_plural': '\u0417\u0430\u043a\u0430\u0437\u044b',
            },
        ),
        migrations.RunPython(create_items, reverse_code=migrations.RunPython.noop),
    ]
