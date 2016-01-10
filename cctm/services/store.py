# -*- coding:utf-8 -*-
import logging
from collections import OrderedDict
from cctm import json
from cctm.path import safe_open
from .resolver import Resolver
logger = logging.getLogger(__name__)


class PackagesStore(object):
    def __init__(self, config, path=None):
        self.config = config
        self.path = path or self.config.store_path

    def load(self):
        try:
            with safe_open(self.path, "r") as rf:
                return json.load(rf)
        except FileNotFoundError:
            return []

    def update(self, package_data, exists_data):
        store_data = [package_data]
        store_data.extend(self.remove(package_data["name"], exists_data))
        return store_data

    def remove(self, name, exists_data):
        return [d for d in exists_data if d["name"] != name]

    def save(self, store_data):
        with open(self.path, "w") as wf:
            json.dump(store_data, wf)


class RepositoriesStore(object):
    def __init__(self, config):
        self.config = config
        self.resolver = Resolver(self.config)

    def load(self):
        return self.config.repositories

    def extract_packages(self, repositories=None):
        repositories = repositories or self.load()
        d = OrderedDict()

        for stored_url in repositories:
            logger.info("merging %s", stored_url)
            asset = self.resolver.resolve(stored_url)
            for data in asset.json():
                d[data["name"]] = data
        return list(d.values())
