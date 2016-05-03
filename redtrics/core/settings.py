# -*- coding: utf-8 -*-

import imp

from default_settings import *  # NOQA

imp.load_source('my_settings', '/opt/redtrics/etc/settings.py')
from my_settings import *  # NOQA
