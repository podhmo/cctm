# -*- coding:utf-8 -*-
import os.path
from cached_property import cached_property as reify
from cctm.path import safe_listdir
from . import PackagesStore


def normalize(name):
    return name.lower().replace("_", "").replace("-", "")


class InstalledPackageLookup(object):
    def __init__(self, config):
        self.config = config

    def load(self):
        r = []
        for path in safe_listdir(self.config.template_dir):
            basename = path.replace(".", "/")
            r.append({
                "name": basename,
                "path": os.path.join(self.config.template_dir, path)
            })
        return r

    def lookup_loose(self, name, exists_data=None):
        exists_data = exists_data or self.load()
        return lookup_loose(name, exists_data)

    def lookup(self, name, exists_data=None):
        exists_data = exists_data or self.load()
        return lookup(name, exists_data)


class PackageLookup(object):
    def __init__(self, config):
        self.config = config

    @reify
    def store(self):
        return PackagesStore(self.config)

    def load(self):
        return self.store.load()

    def lookup_loose(self, name, exists_data=None):
        exists_data = exists_data or self.load()
        return lookup_loose(name, exists_data)

    def lookup(self, name, exists_data=None):
        exists_data = exists_data or self.load()
        return lookup(name, exists_data)


def lookup(name, exists_data):
    for d in exists_data:
        package_name = d["name"]
        if package_name == name:
            return d


def lookup_loose(name, exists_data):
    name = normalize(name)
    for d in exists_data:
        package_name = normalize(d["name"])
        if package_name == name:
            return d
        try:
            if package_name.split("/")[1] == name:
                return d
        except IndexError:
            pass
