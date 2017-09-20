# -*- coding: utf-8 -*-

import os
from distutils.core import setup
from setuptools import find_packages

__author__ = 'Alexei Kuzmin'
__version__ = "0.9.15"

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-yandex-kassa',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/DrMartiner/django-yandex-kassa',
    license='MIT',
    author=__author__,
    author_email='DrMartiner@GMail.Com',
    keywords=['django', 'yandex', 'money', 'kassa', 'payment',
              'pay', 'payment', 'ecommerce', 'shop', 'cart'],
    description='Integrating django project with yandex-kassa',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>1.6',
        'six',
    ],
    extras_require={
        'dev': [
            'ecdsa==0.13',
            'pycrypto==2.6.1',
        ]
    },
)
