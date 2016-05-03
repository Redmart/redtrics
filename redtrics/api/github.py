# -*- coding: utf-8 -*-

from application.python.types import Singleton
from github3 import login

from ..core.settings import github_token, github_organization


class GithubApi(object):
    __metaclass__ = Singleton

    def __init__(self):
        self.client = login(token=github_token)

    def repos(self):
        try:
            return self._repos.values()
        except:
            self._repos = dict(
                (repo.name, repo) for repo in self.client.organization(login=github_organization).iter_repos())
            return self._repos.values()

    def repo(self, name):
        return self._repos.get(name)

    def commit(self, repo, sha):
        return self._repos.get(repo).commit(sha)
