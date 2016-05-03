# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from pytz import utc


class DateUtils(object):

    @classmethod
    def one_week_ago(self):
        return utc.localize(datetime.now() - timedelta(days=7))

    @classmethod
    def parse(self, date_string, format):
        return utc.localize(datetime.strptime(date_string, format))
