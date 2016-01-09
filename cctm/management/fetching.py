# -*- coding:utf-8 -*-
import json
import requests
from handofcats import as_command
from dictremapper import Remapper, Path


def get_fullname(repository):
    if "://" in repository:
        url = repository
        return "/".join(url.rstrip("/").split("/")[-2:])
    return repository


class Namespace(object):
    baseurl = "https://api.github.com"

    def __init__(self, fullname):
        self.fullname = fullname  # fullname is ":owner/:name"

    @property
    def versions_url(self):
        urlfmt = "{self.baseurl}/repos/{self.fullname}/tags"
        return urlfmt.format(self=self)

    @property
    def summary_url(self):
        urlfmt = "{self.baseurl}/repos/{self.fullname}"
        return urlfmt.format(self=self)


class GithubSummaryRemapper(Remapper):
    name = Path("full_name")
    url = Path("html_url")
    description = Path("description")
    created_at = Path("created_at")
    updated_at = Path("updated_at")
    star = Path("stargazers_count")


@as_command
def main(repository, show_all=False):
    full_name = get_fullname(repository)
    data = requests.get(Namespace(full_name).summary_url).json()
    if not show_all:
        remapper = GithubSummaryRemapper()
        data = remapper(data)
    print(json.dumps(data, indent=2))
