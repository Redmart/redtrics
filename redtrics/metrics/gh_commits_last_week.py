# -*- coding: utf-8 -*-

from datetime import timedelta
from influxdb import SeriesHelper
from redtrics.api.influxdbapi import InfluxDBApi
from redtrics.api.github import GithubApi
from redtrics.utils.dateutils import DateUtils
from redtrics.metrics.registry import MetricRegistry
from .base import BaseMetric


class CommitsLastWeekSeriesHelper(SeriesHelper):
    class Meta:
        series_name = 'commits_last_week'
        fields = ['commits', 'additions', 'deletions', 'biggest']
        tags = ['base']


@MetricRegistry.register
class CommitsLastWeek(BaseMetric):
    name = 'commits_last_week'
    description = "Commits Last week"

    def __init__(self):
        BaseMetric.__init__(self)
        self.gh = GithubApi()
        self.influxdb = InfluxDBApi()

    def _retrieve_data(self):

        self.commits = []

        for repo in self.gh.repos():
            self.logger.debug("Retrieving commit info for: repo {} - branch {}".format(repo, self.base))
            try:
                for commit in repo.iter_commits(self.base, since=DateUtils.one_week_ago() + timedelta(days=1)):
                    self.commits.append(self.gh.commit(repo.name, commit.sha))
            except:
                self.logger.debug("{0} is empty in {1}".format(repo, self.base))

    def _compute(self):
        self.results = {
            'commits': len(self.commits),
            'additions': 0,
            'deletions': 0,
            'biggest': 0
        }
        for c in self.commits:
            self.results['additions'] += c.additions
            self.results['deletions'] += c.deletions
            self.results['biggest'] = max(self.results['biggest'], c.additions + c.deletions)

    def _write_results(self):
        CommitsLastWeekSeriesHelper(base=self.base, **self.results)
        CommitsLastWeekSeriesHelper.commit(self.influxdb.client)
