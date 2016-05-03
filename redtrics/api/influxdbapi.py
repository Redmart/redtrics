# -*- coding: utf-8 -*-

from redtrics.core.settings import influxdb_settings
from application.python.types import Singleton
from influxdb import InfluxDBClient


class InfluxDBApi(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.client = InfluxDBClient(host=influxdb_settings['host'], username=influxdb_settings['username'],
                                     password=influxdb_settings['password'], database=influxdb_settings['database'])
