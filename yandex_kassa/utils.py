# -*- coding: utf-8 -*-

from uuid import uuid4

from django.shortcuts import _get_queryset


def get_uuid():
    return str(uuid4()).replace('-', '')


def get_object_or_None(klass, *args, **kwargs):
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
