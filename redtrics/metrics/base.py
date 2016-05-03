# -*- coding: utf-8 -*-

import logging


class BaseMetric(object):
    name = None

    def _retrieve_data(self):
        pass

    def _compute(self):
        pass

    def _write_results(self):
        pass

    def __init__(self):
        pass

    def run(self, base='master'):
        self.base = base
        self.logger = logging.getLogger(__name__)
        self.logger.info("{} Started".format(self.description))
        self._retrieve_data()
        self._compute()
        self._write_results()
        self.logger.info("{} Stopped".format(self.description))
        return self.results
