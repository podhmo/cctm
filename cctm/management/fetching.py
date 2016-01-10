# -*- coding:utf-8 -*-
import requests
from dictremapper import Remapper, Path
from cctm import services
from cctm import json


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


def main(config, repository, show_all=False, save=False, store=None):
    full_name = get_fullname(repository)
    data = requests.get(Namespace(full_name).summary_url).json()
    if not show_all:
        remapper = GithubSummaryRemapper()
        data = remapper(data)

    if not save:
        print(json.dumps(data))
    else:
        store = services.PackagesStore(config, path=store)
        store_data = store.update(data, store.load())
        store.save(store_data)


def includeme(config):
    config.register_command("management.fetch", main)
