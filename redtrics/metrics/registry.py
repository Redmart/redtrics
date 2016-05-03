# -*- coding: utf-8 -*-


class MetricRegistry(object):
    METRICS_LIST = []

    @staticmethod
    def register(cls):
        """
        Class decorator for adding plugins to the registry
        """
        if cls not in MetricRegistry.METRICS_LIST:
            MetricRegistry.METRICS_LIST.append(cls())
        return cls
