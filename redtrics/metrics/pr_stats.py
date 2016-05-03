# -*- coding: utf-8 -*-

from influxdb import SeriesHelper
from numpy import mean
from redtrics.api.influxdbapi import InfluxDBApi
from redtrics.api.github import GithubApi
from redtrics.metrics.registry import MetricRegistry
from redtrics.utils.dateutils import DateUtils
from .base import BaseMetric


class PullRequestAgeSeriesHelper(SeriesHelper):
    class Meta:
        series_name = 'pr_age_closed'
        fields = ['max', 'min', 'avg']
        tags = ['base']


class PullRequestCommitsSeriesHelper(SeriesHelper):
    class Meta:
        series_name = 'pr_commits_closed'
        fields = ['pr_count', 'commits_count', 'additions', 'deletions', 'biggest']
        tags = ['base']


@MetricRegistry.register
class PullRequestStats(BaseMetric):
    name = "pr_stats"
    description = "Pull Requests Stats"
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

    def __init__(self):
        BaseMetric.__init__(self)
        self.gh = GithubApi()
        self.influxdb = InfluxDBApi()

    def _retrieve_data(self):
        self.closed_pull_requests = []
        self.open_pull_requests = []
        for repo in self.gh.repos():
            for pr in repo.iter_pulls(state="all", base=self.base):
                if pr.state == "closed" and pr.closed_at > DateUtils.one_week_ago():
                    self.closed_pull_requests.append(repo.pull_request(pr.number))
                elif pr.state == "open" and pr.created_at <= DateUtils.one_week_ago():
                    self.open_pull_requests.append(repo.pull_request(pr.number))

    def _compute(self):
        self.results = {'closed': {}, 'open': {}}
        pr_age = map(lambda pr: (pr.closed_at - pr.created_at).seconds, self.closed_pull_requests)
        self.results['closed']['age'] = {'max': max(pr_age), 'min': min(pr_age), 'avg': mean(pr_age)}
        self.results['closed']['commits'] = {
            'pr_count': len(pr_age),
            'commits_count': 0,
            'additions': 0,
            'deletions': 0,
            'biggest': 0
        }
        for p in self.closed_pull_requests:
            for c in p.iter_commits():
                commit = self.gh.commit(p.repository[1], c.sha)
                if DateUtils.parse(commit.commit.author['date'], self.DATE_FORMAT) > DateUtils.one_week_ago():
                    self.results['closed']['commits']['commits_count'] += 1
                    self.results['closed']['commits']['additions'] += commit.additions
                    self.results['closed']['commits']['deletions'] += commit.deletions
                    self.results['closed']['commits']['biggest'] = max(
                        self.results['closed']['commits']['biggest'],
                        commit.additions + commit.deletions)

        self.results['open'] = self.open_pull_requests

    def _write_results(self):
        PullRequestAgeSeriesHelper(base=self.base, **self.results['closed']['age'])
        PullRequestCommitsSeriesHelper(base=self.base, **self.results['closed']['commits'])
        PullRequestAgeSeriesHelper.commit(self.influxdb.client)
        PullRequestCommitsSeriesHelper.commit(self.influxdb.client)
