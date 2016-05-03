# -*- coding: utf-8 -*-

from babel import dates


def format_datetime(value, format='medium'):
    return dates.format_datetime(value, format, locale='en')
