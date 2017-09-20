django-yandex-kassa
===================

`Документация <https://money.yandex.ru/doc.xml?id=527069>`_ по интеграции


Оформление документов
---------------------

#. Идем на `kassa.yandex.ru <https://kassa.yandex.ru>`_

#. Регистрируемся

#. Созваниваемся с сапортом, отправляем сканы, получаем SCID & ShopID

Отдельно нужно договариваться (писать прошение, подавать доп. пакет документов) на прием платежей через

* Сбер, т.к. он не умеет делать возврат и, вообще, особенный;
* мобильные платежи: на момент написания документации для подключения 'ого способа оплаты сайт должен был иметь оборотку более 30тр в месяц +процент для каждого оператора оговаривается отдельно;
* QiWi;
* MasterPass.


Установка
---------

#.  Установить пакет:

    .. code:: sh

        pip install django-yandex-kassa

#.  Добавить ``yandex_kassa`` в ``settings.INSTALLED_APPS``:

    .. code:: python

        INSTALLED_APPS = (
            ...
            'yandex_kassa',
            ...
        )

#. Выполнить синхронизацию с БД:

    .. code:: sh

        python manage.py syncdb

#. Добавить в ``urls.py``:

    .. code:: python

        urlpatterns = patterns('',
            # ...
            url(r'^kassa/', include('yandex_kassa.urls')),
        )

#. Указать в settings следующие параметры:

    .. code:: python
    
        YANDEX_KASSA_DEBUG = False
        YANDEX_KASSA_SCID = 123123
        YANDEX_KASSA_SHOP_ID = 123123
        YANDEX_KASSA_SHOP_PASSWORD = 'password'

        YANDEX_KASSA_DISPLAY_FIELDS = ['paymentType', 'cps_email', 'cps_phone']

        YANDEX_KASSA_CALLBACK_URL = '/kassa/callback/'
        YANDEX_KASSA_FAIL_URL = '/kassa/fail/'
        YANDEX_KASSA_SUCCESS_URL = '/kassa/success/'

        YANDEX_KASSA_PAYMENT_TYPE = ['AB', 'AC', 'GP', 'PB', 'PC', 'WM']


#. Указать в рабочем Яндекс Кассы кабинете натсрйоки для приема уведомлений:

* paymentAvisoURL: https://example.com/kassa/payment-aviso/
* checkURL: https://example.com/kassa/order-check/
* failURL: https://example.com/kassa/fail/
* successURL: https://example.com/kassa/success/


Использование
-------------

`Полный пример использования <https://github.com/DrMartiner/django-yandex-kassa/tree/master/demo>`_

#. Реализуйте представление и модель товара и заказа:

    .. code:: python

        # -*- coding: utf-8 -*-

        # ...

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

    .. code:: python

        # -*- coding: utf-8 -*-

        # ...

        class Item(models.Model):
            name = models.CharField('Наименование', max_length=32)
            price = models.PositiveIntegerField('Стоимость')

            def __unicode__(self):
                return truncatechars(self.name, 16)

            class Meta:
                verbose_name = 'Товар'
                verbose_name_plural = 'Товары'


        class Order(models.Model):
            uuid = models.CharField('ID заказа', max_length=64,
                                    default=get_uuid, primary_key=True)
            item = models.ForeignKey('app.Item', verbose_name='Товар')
            count = models.PositiveIntegerField('Кол-во', default=1)
            payment = models.ForeignKey('yandex_kassa.Payment',
                                        verbose_name='Платеж')
            amount = models.PositiveIntegerField('Сумма заказа')

            class Meta:
                verbose_name = 'Заказ'
                verbose_name_plural = 'Заказы'


#. Шаблон платежной формы:

    .. code:: html

        <div class="col-lg-6 col-md-6 col-sm-6 col-xs-6">
            <form action="{{ form.target }}"
                  method="post" class="form" name="ShopForm" id="payment_form_id">
                {% bootstrap_form form %}

                {% buttons %}
                    <button type="submit" class="btn btn-success">
                        {% bootstrap_icon "shopping-cart" %}
                        Оплатить "{{ order.item.name }}" x{{ order.count }} шт
                    </button>
                {% endbuttons %}
            </form>
        </div>

