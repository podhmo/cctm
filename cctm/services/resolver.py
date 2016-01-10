# -*- coding:utf-8 -*-
import os.path
import requests
from cctm import json


class Resolver(object):
    def __init__(self, config):
        self.config = config

    def resolve(self, path):
        if path.startswith("file://"):
            return File(path[7:])
        elif path.startswith(("http://", "https://")):
            return URL(path)
        else:
            return File(path)


class Asset(object):
    def __init__(self, path):
        self.path = os.path.expanduser(path)


class File(Asset):
    def json(self):
        with open(self.path) as rf:
            return json.load(rf)


class URL(Asset):
    def json(self):
        return requests.get(self.path).json()
