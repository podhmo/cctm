# -*- coding:utf-8 -*-
from cctm import json
import os.path
import logging
from miniconfig_argparse import Configurator as ConfiguratorCore
from miniconfig_argparse import ParserTreeControl as Control
from cached_property import cached_property as reify
from .path import pickup_file, safe_open
logger = logging.getLogger(__name__)


class CCTMControl(Control):
    DEFAULT_BASE_PATH = "~/.cctm/"

    def resolve_path(self, target_file):
        path = pickup_file(self.current_path, target_file) or os.path.join(self.base_path, target_file)
        return os.path.abspath(path)

    @reify
    def base_path(self):
        return os.path.expanduser(self.settings.get("base_path", self.DEFAULT_BASE_PATH))

    @reify
    def current_path(self):
        return self.settings.get("current_path") or os.getcwd()

    @reify
    def config_path(self):
        return self.resolve_path("cctm.json")

    @reify
    def store_path(self):
        return self.resolve_path("store.json")

    @reify
    def template_dir(self):
        return self.resolve_path("templates")

    @reify
    def repositories(self):
        return self.settings.get("repositories") or []


class Configurator(ConfiguratorCore):
    def __init__(self, settings=None, module=None, control=None):
        settings = settings or {}
        control = control or CCTMControl(settings)
        super(Configurator, self).__init__(settings, module, control)

    def set_value(self, k, v):
        setattr(self.control, k, v)


def load_config(config, path=None):
    path = path or config.config_path
    if not os.path.exists(path):
        logger.info("%s is not found. create as default configuration")
        config.init_config(path=path)

    with open(path) as rf:
        config.settings = config.control.settings = settings = json.load(rf)  # xxx
        return settings


def save_config(config, settings, path=None):
    path = path or config.config_path
    with safe_open(path, "w") as wf:
        json.dump(settings, wf)


def includeme(config):
    config.add_directive("load_config", load_config)
    config.add_directive("save_config", save_config)
