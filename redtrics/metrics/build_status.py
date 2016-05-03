# -*- coding: utf-8 -*-

from itertools import ifilter
from influxdb import SeriesHelper
from redtrics.api.github import GithubApi
from redtrics.api.influxdbapi import InfluxDBApi
from redtrics.metrics.registry import MetricRegistry
from redtrics.utils.dateutils import DateUtils
from .base import BaseMetric


class BuildStatusSeriesHelper(SeriesHelper):
    class Meta:
        series_name = 'build_status'
        fields = ['success', 'failure']
        tags = ['base']


@MetricRegistry.register
class BuildStatus(BaseMetric):
    name = 'build_status'
    description = "Build Status"

    def __init__(self):
        BaseMetric.__init__(self)
        self.gh = GithubApi()
        self.influxdb = InfluxDBApi()

    def _retrieve_data(self):
        self.status = []
        for repo in self.gh.repos():
            self.logger.debug("Retrieving build status for: repo {} - branch {}".format(repo, self.base))
            for status in repo.iter_statuses(self.base):
                if status.created_at <= DateUtils.one_week_ago():
                    break
                self.status.append(status)

    def _compute(self):
        self.results = {'success': len(list(ifilter(lambda s: s.state == "success", self.status))),
                        'failure': len(list(ifilter(lambda s: s.state == "failure", self.status)))
                        }

    def _write_results(self):
        BuildStatusSeriesHelper(base=self.base, **self.results)
        BuildStatusSeriesHelper.commit(self.influxdb.client)
